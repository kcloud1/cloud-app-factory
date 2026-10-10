"""Generate a read-only, cloud-first app handoff from four short answers."""

import argparse
import json
import re
import sys
from pathlib import Path

from factory import InvalidIntake, plan, slug

FACTORY_REPOSITORY = "kcloud1/cloud-app-factory"


def draft(app, purpose, hostname, budget, factory_revision):
    name = slug(app)
    if not isinstance(factory_revision, str) or not re.fullmatch(r"[0-9a-f]{40}", factory_revision):
        raise InvalidIntake("Expected a reviewed full 40-character factory SHA")
    if not isinstance(purpose, str) or not purpose.strip() or len(purpose) > 200 or any(c in purpose for c in "\r\n<>"):
        raise InvalidIntake("Use a short public description without markup/newlines")
    host = hostname or f"{name}.amitk.life"
    if host != f"{name}.amitk.life":
        raise InvalidIntake("Fast path allows only the exact app.amitk.life hostname")
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
    proposed = plan(intake)
    if proposed["execution_allowed"]:
        raise InvalidIntake("Planning must never authorize execution")
    task = f"""# Codex Cloud handoff — {name}

This is a PROPOSAL, not permission to create a public app, domain or Worker.

- Owning factory: https://github.com/{FACTORY_REPOSITORY}
- Parent milestone: https://github.com/{FACTORY_REPOSITORY}/issues/4
- Request ID: {proposed['plan_id']}
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
        "CODEX_CLOUD_GO.md": task,
        ".factory/intake.json": json.dumps(intake, indent=2, sort_keys=True) + "\n",
        ".github/workflows/factory-plan.yml": caller,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", required=True)
    parser.add_argument("--purpose", required=True, help="Public text only; no secrets")
    parser.add_argument("--hostname", default="", help="Defaults to app.amitk.life")
    parser.add_argument("--budget", default="0", help="Only $0 in this fast path")
    parser.add_argument("--factory-revision", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        output = draft(args.app, args.purpose, args.hostname, args.budget, args.factory_revision)
        dest = Path(args.out).resolve()
        for path, data in output.items():
            target = (dest / path).resolve()
            if not target.is_relative_to(dest):
                raise InvalidIntake("Output must remain in the selected directory")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(data)
    except (InvalidIntake, ValueError, OSError):
        print("Bootstrap input invalid or output unavailable. No provider actions taken.", file=sys.stderr)
        return 2
    print("PLAN_ONLY: generated deterministic Codex Cloud handoff and read-only caller")
    return 0


if __name__ == "__main__":
    sys.exit(main())
