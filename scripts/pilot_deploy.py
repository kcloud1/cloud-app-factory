"""Trusted pilot preflight and Actions-only publication. No caller code runs here."""

import argparse
import fnmatch
import json
import os
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from pilot_artifact import require, validate

ACCOUNT = "7b5b3463a1c5453f4805289b5f42c110"
ZONE = "c7fa361e205bc82159405b27b4ff3fce"
WORKER = "factory-pilot"
HOSTNAME = "factory-pilot.amitk.life"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise ValueError("Provider redirect forbidden")


def api_get(path, query=None):
    url = "https://api.cloudflare.com/client/v4" + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(url, headers={"Authorization": "Bearer " + os.environ["CLOUDFLARE_API_TOKEN"]}, method="GET")
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=30) as response:
            document = json.loads(response.read(8 * 1024 * 1024))
        require(isinstance(document, dict) and document.get("success") is True, "Provider GET failed")
        return document
    except (urllib.error.URLError, ValueError):
        # Never include provider response bodies, headers or credentials.
        raise ValueError("Required provider metadata GET unavailable") from None


def listing(get, path, query=None):
    entries = []
    for page in range(1, 101):
        document = get(path, dict(query or {}, page=page, per_page=100))
        result = document.get("result")
        require(isinstance(result, list), "Incomplete provider inventory")
        require(all(isinstance(item, dict) for item in result), "Invalid provider inventory")
        entries.extend(result)
        info = document.get("result_info", {})
        require(isinstance(info, dict), "Invalid inventory pagination")
        pages = info.get("total_pages")
        if pages is not None:
            require(type(pages) is int and 0 <= pages <= 100, "Unknown inventory pagination")
            if page >= pages:
                return entries
        elif "total_count" in info:
            require(type(info["total_count"]) is int, "Invalid inventory count")
            if len(entries) >= info["total_count"]:
                return entries
        elif not info and len(result) < 100:
            return entries
        else:
            require(len(result) == 100, "Unknown inventory completion")
    raise ValueError("Inventory pagination incomplete")


def preflight(get=api_get):
    token = get("/user/tokens/verify").get("result", {})
    require(isinstance(token, dict) and token.get("status") == "active", "Actions token not active")
    for field, future in [("expires_on", True), ("not_before", False)]:
        if token.get(field):
            value = datetime.fromisoformat(token[field].replace("Z", "+00:00"))
            require(value.tzinfo is not None, "Unknown token validity time")
            require((value > datetime.now(timezone.utc)) if future else (value <= datetime.now(timezone.utc)), "Token validity failed")
    account = get("/accounts/" + ACCOUNT).get("result", {})
    require(isinstance(account, dict) and account.get("id") == ACCOUNT and account.get("name") == "dev1", "Wrong account")
    zone = get("/zones/" + ZONE).get("result", {})
    require(isinstance(zone, dict) and zone.get("id") == ZONE and zone.get("name") == "amitk.life" and zone.get("status") == "active" and zone.get("account", {}).get("id") == ACCOUNT, "Wrong zone/account")
    scripts = listing(get, "/accounts/" + ACCOUNT + "/workers/scripts")
    workers = [item for item in scripts if item.get("id") == WORKER]
    require(len(workers) <= 1, "Ambiguous Worker identity")
    if workers:
        tag = workers[0].get("tag")
        require(isinstance(tag, str) and re.fullmatch(r"[0-9a-f]{32}", tag), "Worker tag unavailable for Builds readback")
        triggers = listing(get, "/accounts/" + ACCOUNT + "/builds/workers/" + tag + "/triggers")
        require(not triggers, "Native Builds writer is connected")
        hooks = listing(get, "/accounts/" + ACCOUNT + "/builds/workers/" + WORKER + "/deploy_hooks")
        require(not hooks, "Native Builds deploy hook is connected")
    # A fully observed absent Worker has no Worker tag to attach native Builds to.
    # Never infer disconnection from a 403/404 on an existing Worker's Builds API.
    domains = listing(get, "/accounts/" + ACCOUNT + "/workers/domains")
    bindings = [item for item in domains if item.get("hostname") == HOSTNAME]
    require(len(bindings) <= 1, "Ambiguous hostname binding")
    require(all(item.get("service") == WORKER and item.get("zone_id") == ZONE and item.get("environment") in ["production", None] for item in bindings), "Hostname belongs to another Worker/zone")
    records = listing(get, "/zones/" + ZONE + "/dns_records", {"name": HOSTNAME})
    require(not records or bool(bindings), "Existing DNS without approved Worker binding")
    routes = listing(get, "/zones/" + ZONE + "/workers/routes")
    for route in routes:
        pattern = route.get("pattern")
        require(isinstance(pattern, str), "Unknown route pattern")
        normalized = pattern.removeprefix("https://").removeprefix("http://")
        # Any path on the exact host can intercept an asset/app request.
        route_host = normalized.split("/", 1)[0].lower()
        if fnmatch.fnmatchcase(HOSTNAME, route_host):
            require(route.get("script") == WORKER, "Conflicting zone Worker route")
    return {"account": "dev1", "worker_exists": bool(workers), "native_builds": "unconnected",
            "exact_domain": HOSTNAME, "token_active": True,
            "token_expiration": token.get("expires_on") or "none reported by verify API",
            "observed_at": datetime.now(timezone.utc).isoformat()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--wrangler", type=Path, required=True)
    args = parser.parse_args()
    try:
        require(os.environ.get("GITHUB_ACTIONS") == "true" and os.environ.get("GITHUB_REPOSITORY") == "kcloud1/factory-pilot" and os.environ.get("GITHUB_EVENT_NAME") == "push" and os.environ.get("GITHUB_REF") == "refs/heads/main", "Only the approved Actions push may publish")
        require(os.environ.get("CLOUDFLARE_ACCOUNT_ID") == ACCOUNT and bool(os.environ.get("CLOUDFLARE_API_TOKEN")), "Approved Actions credentials unavailable")
        require(os.environ.get("GITHUB_SHA") == args.sha, "Push SHA mismatch")
        validate(args.artifact, args.sha)
        trusted = Path(__file__).resolve().parents[1] / "deploy-tooling/node_modules/wrangler/bin/wrangler.js"
        require(args.wrangler.resolve() == trusted and trusted.is_file(), "Untrusted deployment tooling")
        evidence = preflight()
        print(json.dumps(evidence, sort_keys=True), flush=True)
        # Revalidate after network observation and immediately bind Wrangler to
        # the generated config. No npm, npx, caller executable or shell involved.
        validate(args.artifact, args.sha)
    except (ValueError, OSError, KeyError):
        raise SystemExit("Pilot live preflight blocked; no deployment attempted")
    subprocess.run(["node", str(trusted), "deploy", "--strict", "--config", str((args.artifact / "wrangler.json").resolve()), "--cwd", str(args.artifact.resolve())], check=True)


if __name__ == "__main__":
    main()
