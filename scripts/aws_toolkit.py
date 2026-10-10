#!/usr/bin/env python3
"""Opt-in Linux tooling; never authenticates or invokes AWS service commands."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile

PROFILES = Path(__file__).resolve().parents[1] / "env/aws-toolkit"
MANIFEST = json.loads((PROFILES / "versions.json").read_text())
VERSION_ARGS = {"aws": ["--version"], "gh": ["--version"],
                "terraform": ["version", "-json"],
                "session-manager-plugin": ["--version"], "ampx": ["--version"]}


def architecture():
    arch = {"x86_64": "amd64", "aarch64": "arm64"}.get(platform.machine())
    if platform.system() != "Linux" or not arch or platform.libc_ver()[0] != "glibc":
        raise ValueError("Supported: Linux glibc x86_64/aarch64. No system changes made.")
    return arch


def clean_env(home):
    # Construct an allowlist, rather than copying environment credentials/config.
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(home),
            "LANG": "C.UTF-8", "AWS_CONFIG_FILE": "/dev/null",
            "AWS_SHARED_CREDENTIALS_FILE": "/dev/null",
            "AWS_EC2_METADATA_DISABLED": "true", "AWS_PAGER": "",
            "GH_CONFIG_DIR": str(home / "gh"), "CHECKPOINT_DISABLE": "1",
            "NPM_CONFIG_USERCONFIG": str(home / "user.npmrc"),
            "NPM_CONFIG_GLOBALCONFIG": str(home / "global.npmrc"),
            "NPM_CONFIG_CACHE": str(home / "npm-cache"),
            "NPM_CONFIG_IGNORE_SCRIPTS": "true", "NPM_CONFIG_AUDIT": "false",
            "NPM_CONFIG_FUND": "false", "NPM_CONFIG_REGISTRY": "https://registry.npmjs.org/",
            "AMPLIFY_DISABLE_TELEMETRY": "1", "CI": "true"}


def run(argv, cwd=None, timeout=60):
    with tempfile.TemporaryDirectory(prefix="aws-toolkit-check-") as tmp:
        home = Path(tmp)
        result = subprocess.run([str(a) for a in argv], env=clean_env(home),
                                cwd=cwd or home, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=timeout)
        if result.returncode:
            # Errors never reproduce caller environment or command output.
            raise ValueError(f"{Path(argv[0]).name} failed (exit {result.returncode}); no authentication attempted")
        return result.stdout.strip()


def version(name, executable):
    if name == "ampx":
        # npm supplies the package-manager context required by Gen 2. An exact
        # local executable plus --offline/--no cannot resolve a floating package.
        output = run([shutil.which("npm"), "exec", "--offline", "--no", "--",
                      Path(executable).absolute(), "--version"])
    else:
        output = run([executable, *VERSION_ARGS[name]])
    if name == "terraform":
        return json.loads(output)["terraform_version"]
    match = re.search(r"(?<!\d)(\d+\.\d+\.\d+(?:\.\d+)?)(?!\d)", output)
    if not match:
        raise ValueError(f"Cannot read {name} version")
    return match[1]


def tool_path(name, prefix, project):
    if name == "ampx":
        return project / ".aws-toolkit/app-dev/node_modules/.bin/ampx" if project else None
    managed = prefix / "bin" / name
    return managed if managed.exists() else shutil.which(name)


def inventory(profile, prefix, project):
    result = {}
    for name in MANIFEST["profiles"][profile]:
        path = tool_path(name, prefix, project)
        actual = version(name, path) if path and Path(path).is_file() else None
        pin = MANIFEST["tools"][name]["version"]
        pinned = actual == pin
        if name == "ampx" and pinned:
            pinned = appdev_matches(project / ".aws-toolkit/app-dev")
        result[name] = {"required": pin, "version": actual,
                        "pinned": pinned, "path": str(path) if path else None}
    return result


def prerequisites(profile):
    git = shutil.which("git")
    if not git or sys.version_info < (3, 10):
        raise ValueError("Provide Git and Python >=3.10 in the base image; no sudo/package-manager fallback")
    data = {"git": run([git, "--version"]), "python": platform.python_version()}
    if profile == "cloudops" and not shutil.which("dpkg-deb"):
        raise ValueError("cloudops requires dpkg-deb for extraction only (no package installation)")
    if profile == "app-dev":
        node, npm = shutil.which("node"), shutil.which("npm")
        if not node or not npm:
            raise ValueError("app-dev requires Node 22/24 and npm in the base image")
        node_version = run([node, "--version"])
        if int(node_version.lstrip("v").split(".")[0]) not in (22, 24):
            raise ValueError("app-dev supports Node 22/24 LTS; do not use EOL Node 18/20")
        data.update(node=node_version, npm=run([npm, "--version"]))
    return data


class HTTPSRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not newurl.startswith("https://"):
            raise ValueError("Refusing non-HTTPS download redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(asset, target):
    if not asset["url"].startswith("https://"):
        raise ValueError("HTTPS is required")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), HTTPSRedirect())
    digest = hashlib.sha256()
    with opener.open(asset["url"], timeout=60) as response, target.open("xb") as out:
        while chunk := response.read(1024 * 1024):
            out.write(chunk)
            digest.update(chunk)
    if digest.hexdigest() != asset["sha256"]:
        raise ValueError("Download SHA256 mismatch; nothing extracted or executed")


def member_path(root, name):
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError("Unsafe archive path")
    return root.joinpath(*path.parts)


def extract(archive, target, kind):
    # All archives are hash-verified first; still reject path traversal and links.
    if kind == "zip":
        with zipfile.ZipFile(archive) as files:
            for item in files.infolist():
                path = member_path(target, item.filename)
                mode = item.external_attr >> 16
                if stat.S_ISLNK(mode):
                    raise ValueError("Archive links are unsupported")
                if item.is_dir():
                    path.mkdir(parents=True, exist_ok=True)
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with files.open(item) as src, path.open("xb") as dst:
                        shutil.copyfileobj(src, dst)
                    path.chmod(0o755 if mode & 0o111 else 0o644)
    elif kind == "tar":
        with tarfile.open(archive) as files:
            for item in files:
                path = member_path(target, item.name)
                if item.isdir():
                    path.mkdir(parents=True, exist_ok=True)
                elif item.isfile():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with files.extractfile(item) as src, path.open("xb") as dst:
                        shutil.copyfileobj(src, dst)
                    path.chmod(0o755 if item.mode & 0o111 else 0o644)
                else:
                    raise ValueError("Archive links/devices are unsupported")
    else:
        run([shutil.which("dpkg-deb"), "--extract", archive, target])
        # Extracting never registers the package or starts its bundled service.


def install_binary(name, prefix, arch, existing):
    if existing["pinned"]:
        return "REUSED"
    tool = MANIFEST["tools"][name]
    destination = prefix / f"{name}-{tool['version']}-{arch}"
    link = prefix / "bin" / name
    if link.exists() or link.is_symlink() or destination.exists():
        raise ValueError(f"Managed {name} collision; inspect/rollback it before installation")
    with tempfile.TemporaryDirectory(prefix=".stage-", dir=prefix) as tmp:
        stage = Path(tmp)
        archive, content = stage / "download", stage / "content"
        content.mkdir()
        download(tool["assets"][arch], archive)
        extract(archive, content, tool["format"])
        executable = content / tool["executable"].format(arch=arch)
        if version(name, executable) != tool["version"]:
            raise ValueError(f"Verified download has an unexpected {name} version")
        # Keep only the SSM client; do not retain service/init configuration.
        if name == "session-manager-plugin":
            retained = stage / "client"
            retained.mkdir()
            shutil.copy2(executable, retained / name)
            executable = retained / name
            content = retained
        relative = executable.relative_to(content)
        content.rename(destination)
        link.symlink_to(destination / relative)
    return "INSTALLED"


def appdev_matches(target):
    return all((target / name).is_file() and
               (target / name).read_bytes() == (PROFILES / "app-dev" / name).read_bytes()
               for name in ("package.json", "package-lock.json"))


def install_appdev(project, existing):
    target = project / ".aws-toolkit/app-dev"
    if target.parent.is_symlink() or target.is_symlink():
        raise ValueError("app-dev tooling directories must not be symlinks")
    if target.exists():
        if not appdev_matches(target):
            raise ValueError("Existing app-dev package/lock differs; no project files overwritten")
        if existing["pinned"]:
            return "REUSED"
        raise ValueError("Incomplete app-dev install; remove only the reviewed tooling directory to retry")
    target.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".app-dev-stage-", dir=target.parent) as tmp:
        stage = Path(tmp)
        for name in ("package.json", "package-lock.json"):
            shutil.copyfile(PROFILES / "app-dev" / name, stage / name)
        run([shutil.which("npm"), "ci", "--ignore-scripts", "--no-audit", "--no-fund"],
            cwd=stage, timeout=1200)
        if version("ampx", stage / "node_modules/.bin/ampx") != MANIFEST["tools"]["ampx"]["version"]:
            raise ValueError("Unexpected project-local ampx version")
        stage.rename(target)
    return "INSTALLED"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--plan", choices=MANIFEST["profiles"], help="no downloads (default core)")
    mode.add_argument("--check", choices=MANIFEST["profiles"], help="version checks only")
    mode.add_argument("--install", choices=MANIFEST["profiles"], help="explicit opt-in")
    parser.add_argument("--prefix", type=Path,
                        default=Path.home() / ".local/share/cloud-app-factory/aws-toolkit")
    parser.add_argument("--project-dir", type=Path, help="required existing project for app-dev")
    args = parser.parse_args()
    profile = args.install or args.check or args.plan or "core"
    try:
        arch = architecture()
        project = args.project_dir.resolve() if args.project_dir else None
        if profile == "app-dev" and (not project or not project.is_dir()):
            raise ValueError("app-dev requires --project-dir pointing to an existing authorized project")
        prefix = args.prefix.resolve()
        base = prerequisites(profile)
        tools = inventory(profile, prefix, project)
        actions = {}
        if args.install:
            prefix.mkdir(parents=True, exist_ok=True)
            with (prefix / ".install.lock").open("a") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                (prefix / "bin").mkdir(exist_ok=True)
                for name in MANIFEST["profiles"][profile]:
                    actions[name] = (install_appdev(project, tools[name]) if name == "ampx" else
                                     install_binary(name, prefix, arch, tools[name]))
                tools = inventory(profile, prefix, project)
        receipt = {"profile": profile, "platform": f"linux-{arch}", "prerequisites": base,
                   "mode": "install" if args.install else "check" if args.check else "plan",
                   "tools": tools, "actions": actions, "aws_auth": "NOT_ATTEMPTED",
                   "aws_resources": "UNTOUCHED", "path_for_this_task": str(prefix / "bin")}
        print(json.dumps(receipt, indent=2))
        return 0 if not (args.check or args.install) or all(t["pinned"] for t in tools.values()) else 1
    except (ValueError, OSError, subprocess.TimeoutExpired, KeyError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
