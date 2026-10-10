"""Factory-owned validation of the pilot's inert static release artifact."""

import argparse
import json
import re
import shutil
import stat
from pathlib import Path

CONFIG = {
    "name": "factory-pilot", "compatibility_date": "2026-10-10",
    "workers_dev": False, "preview_urls": False,
    "assets": {"directory": "./dist", "html_handling": "auto-trailing-slash", "not_found_handling": "404-page"},
    "routes": [{"pattern": "factory-pilot.amitk.life", "custom_domain": True}],
}
ASSETS = {"index.html", "404.html", "_headers", "app.js", "style.css", "favicon.svg", "release.json"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path, jsonc=False):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "Duplicate config field")
            result[key] = value
        return result
    raw = path.read_text()
    if jsonc:
        raw = re.sub(r",(\s*[}\]])", r"\1", raw)
    return json.loads(raw, object_pairs_hook=unique)


def validate(root, sha, source=False):
    require(re.fullmatch(r"[0-9a-f]{40}", sha), "Exact source SHA required")
    require(not root.is_symlink(), "Symlink release root")
    require(not (root / ".wrangler").exists(), "Generated Wrangler redirect/state forbidden")
    if source:
        config = read_json(root / "wrangler.jsonc", jsonc=True)
        config.pop("$schema", None)
        require(config == CONFIG, "Unapproved Worker/domain/endpoint/configuration")
    else:
        require(set(p.name for p in root.iterdir()) == {"dist", "wrangler.json"}, "Unexpected release artifact entry")
        require(stat.S_ISREG((root / "wrangler.json").lstat().st_mode), "Symlink or nonregular deploy config")
        require(read_json(root / "wrangler.json") == CONFIG, "Changed release configuration")
    directory = root / "dist"
    require(directory.is_dir() and not directory.is_symlink(), "Invalid assets root")
    require(set(p.name for p in directory.iterdir()) == ASSETS, "Unexpected static assets")
    for path in directory.iterdir():
        require(stat.S_ISREG(path.lstat().st_mode), "Symlink or nonregular asset")
        require(path.stat().st_size <= 2 * 1024 * 1024, "Asset exceeds pilot size limit")
    release = read_json(directory / "release.json")
    require(isinstance(release, dict) and set(release) == {"marker", "source_sha", "data", "pipeline"}, "Invalid release receipt")
    require(isinstance(release["marker"], str) and re.fullmatch(r"factory-pilot-v[1-9][0-9]*", release["marker"]), "Invalid release marker")
    require(release["source_sha"] == sha and release["data"] == "fictional" and release["pipeline"] == "github-actions", "Release SHA/data/pipeline mismatch")
    require(sha in (directory / "index.html").read_text(), "HTML lacks exact release SHA")
    return release


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("sha")
    parser.add_argument("--prepare", type=Path, help="Copy only allowlisted static files and factory-generated config")
    args = parser.parse_args()
    try:
        validate(args.root, args.sha, source=args.prepare is not None)
        if args.prepare is not None:
            require(not args.prepare.exists(), "Artifact output already exists")
            args.prepare.mkdir(parents=True)
            shutil.copytree(args.root / "dist", args.prepare / "dist")
            (args.prepare / "wrangler.json").write_text(json.dumps(CONFIG, indent=2) + "\n")
            validate(args.prepare, args.sha)
    except (ValueError, OSError):
        raise SystemExit("Pilot artifact validation failed; no credentials used")
    print("Exact approved Worker/domain/config and static source SHA verified")


if __name__ == "__main__":
    main()
