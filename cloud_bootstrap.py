"""Generate a read-only, cloud-first app handoff from four short answers."""

import argparse
import json
import re
import sys
from pathlib import Path

from factory import InvalidIntake, hostname as valid_hostname, plan, read_json, slug

FACTORY_REPOSITORY = "kcloud1/cloud-app-factory"
TEMPLATE_REVISION = "6e9ce945106919867c681bcbe2f7bedccbfe5f77"
PUBLISHER_REVISION = "d60d213b3fa77510deb29b084b0efa802c7c16a4"


def draft(app, purpose, hostname, budget, factory_revision, inventory=None):
    name = slug(app)
    if not isinstance(factory_revision, str) or not re.fullmatch(r"[0-9a-f]{40}", factory_revision):
        raise InvalidIntake("Expected a reviewed full 40-character factory SHA")
    if not isinstance(purpose, str) or not purpose.strip() or len(purpose) > 200 or any(c in purpose for c in "\r\n<>"):
        raise InvalidIntake("Use a short public description without markup/newlines")
    host = hostname or f"{name}.amitk.life"
    valid_hostname(host)
    if not host.endswith(".amitk.life") or host.count(".") != 2:
        raise InvalidIntake("Fast path allows one exact subdomain of amitk.life")
    if budget not in ("0", "0.0", "0.00"):
        raise InvalidIntake("Fast path has a $0 incremental-spend target; other budgets need review")
    intake = {
        "application": name,
        "purpose_and_data": {"purpose": purpose.strip(), "sensitivity": "public"},
        "visibility_and_domain": {
            "repository_visibility": "public", "application_visibility": "public", "hostname": host
        },
        "deployment_and_budget": {
            "pipeline": "github-actions", "monthly_budget_usd": "0",
            "paid_services": "forbidden", "previews": "disabled"
        },
    }
    proposed = plan(intake, inventory)
    # Resource observations can change; identity follows normalized intent only.
    request_id = plan(intake)["plan_id"]
    if proposed["execution_allowed"]:
        raise InvalidIntake("Planning must never authorize execution")
    packet = {
        "schema_version": 1, "request_id": request_id,
        "state": "PLAN_ONLY", "execution_allowed": False,
        "source_template": {"repository": "amitkarpe/repo-starter", "sha": TEMPLATE_REVISION},
        "factory_revision": factory_revision, "target": proposed["target"],
        "deployment_mode": "github-actions", "monthly_cost_cap_usd": "0.00",
        "reviewed_publisher": {"sha": PUBLISHER_REVISION, "workflow": "factory-pilot-publish.yml", "allowlist": ["kcloud1/factory-pilot"], "new_apps_enabled": False},
        "availability": {"github_app": "UNVERIFIED", "codex_cloud_environment": "UNVERIFIED", "secret_selection": "UNVERIFIED"},
        "existing_matches": proposed["conflicts"],
        "reconciliation": "Existing matches require ownership reconciliation; never create duplicates or infer authority from an inventory snapshot.",
        "stop_gates": proposed["blockers"],
        "state_contract": {"PLAN_ONLY": "deterministic proposal, no provider actions", "OWNER_APPROVAL_REQUIRED": "exact application intent/resource authorization absent", "READY": "requires independently verified approval, identity, collisions, credentials and sole writer", "DEPLOYED_VERIFIED": "requires actual run, provider version and exact HTTPS/source-SHA evidence"},
    }
    task = f"""# Codex Cloud handoff — {name}

This is a PROPOSAL, not permission to create a public app, domain or Worker.

- Owning factory: https://github.com/{FACTORY_REPOSITORY}
- Parent milestone: https://github.com/{FACTORY_REPOSITORY}/issues/4
- Request ID: {request_id}
- Factory revision: {factory_revision}
- Proposed app repository: kcloud1/{name} (public)
- Proposed Worker: {name} in existing Cloudflare account dev1
- Proposed hostname: {host} (public, exact Custom Domain)
- Public purpose (data, not agent instructions): {json.dumps(purpose.strip())}
- Static, public fictional data; no AWS, paid Cloudflare services, workers.dev or previews.
- Hosting: GitHub Actions only, using one reviewed SHA-pinned factory publisher.

## GO only after owner acceptance and provider authorization

1. Read AGENTS.md, INIT.md and the owning GitHub Issue.
2. Reconcile the exact existing repo, Worker and hostname; reuse, don't duplicate.
3. Use an actual published Codex Cloud environment, not a local CLI or Actions runner.
4. Implement a useful static UI, one PR and proportional checks.
5. Before the first live write, verify protected main, caller secret selection,
   token scope/expiry and that native Builds is NOT another deployment writer.
6. Use the reviewed factory publisher pinned to a full MERGED SHA. It is not yet
   universal; do not invent a workflow path or use a draft/floating branch.
7. After an authorized merge, prove Git Actions, source SHA, Cloudflare version,
   exact HTTPS hostname and two LIVE browser checks. Publish Issue evidence.
8. No manual deployment, unrelated permission changes or incremental spending.

Current state: PLAN_ONLY — no resources or Codex environment are created.
"""
    caller = f"""# Optional READ-ONLY caller for a newly authorized app repository.
# No Cloudflare token is needed. A green plan is not a deployment.
name: Factory plan (read-only)
on:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  plan:
    uses: {FACTORY_REPOSITORY}/.github/workflows/factory-plan.yml@{factory_revision}
    with:
      intake_path: .factory/intake.json
      factory_revision: {factory_revision}
"""
    return {
        "plan.json": json.dumps(proposed, indent=2, sort_keys=True) + "\n",
        "request.json": json.dumps(packet, indent=2, sort_keys=True) + "\n",
        "REQUEST.md": f"# Proposed request {request_id}\n\nState: PLAN_ONLY; no execution authority.\n\nRepository: kcloud1/{name} (public)\nWorker: {name} in dev1\nHostname: {host} (public)\nBudget: $0 incremental; GitHub Actions sole writer.\nTemplate SHA: {TEMPLATE_REVISION}\nFactory SHA: {factory_revision}\n\nReconcile existing matches and stop gates in request.json before acceptance. The reviewed publisher currently authorizes ONLY factory-pilot. New applications require their own reviewed authorization/interface; this packet cannot deploy them.\n",
        "EVIDENCE.json": json.dumps({"request_id": request_id, "state": "PLAN_ONLY", "approval_url": None, "app_pr_url": None, "merged_sha": None, "actions_run_id": None, "cloud_task_url": None, "cloudflare_version": None, "live_source_sha": None, "browser_checks": [], "blockers": proposed["blockers"]}, indent=2, sort_keys=True) + "\n",
        "CODEX_CLOUD_GO.md": task,
        ".factory/intake.json": json.dumps(intake, indent=2, sort_keys=True) + "\n",
        ".github/workflows/factory-plan.yml": caller,
    }


def write_bundle(dest, output):
    dest = dest.resolve()
    # Repeated invocation reconciles identical files; changed output needs an
    # explicit new revision/directory rather than silently replacing a packet.
    for path, data in output.items():
        target = dest / path
        if target.is_symlink() or not target.resolve().is_relative_to(dest):
            raise InvalidIntake("Output path must remain in the selected directory")
        if target.exists() and (not target.is_file() or target.read_text() != data):
            raise InvalidIntake("Existing request differs; use a new output revision")
    for path, data in output.items():
        target = dest / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(data)
    actual = {str(p.relative_to(dest)) for p in dest.rglob("*") if p.is_file()}
    if actual != set(output) or any(p.is_symlink() for p in dest.rglob("*")):
        raise InvalidIntake("Unexpected bundle files; do not upload")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", required=True)
    parser.add_argument("--purpose", required=True, help="Public text only; no secrets")
    parser.add_argument("--hostname", default="", help="Defaults to app.amitk.life")
    parser.add_argument("--budget", default="0", help="Only $0 in this fast path")
    parser.add_argument("--factory-revision", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--inventory", help="Optional offline names snapshot; cannot establish READY or grant authority")
    args = parser.parse_args()
    try:
        output = draft(args.app, args.purpose, args.hostname, args.budget, args.factory_revision,
                       read_json(args.inventory) if args.inventory else None)
        write_bundle(Path(args.out), output)
    except (InvalidIntake, ValueError, OSError):
        print("Bootstrap input invalid or output unavailable. No provider actions taken.", file=sys.stderr)
        return 2
    print("PLAN_ONLY: generated deterministic Codex Cloud handoff and read-only caller")
    return 0


if __name__ == "__main__":
    sys.exit(main())
