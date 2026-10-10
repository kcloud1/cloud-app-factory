# No-write release gate

Owning issue: https://github.com/kcloud1/cloud-app-factory/issues/2
Topology: **each selected application repository calls the pinned factory**.
Factory repository credentials do not become the caller's credentials.

## Contract

`release_gate.py` preserves M1. It verifies the plan digest, then regenerates the
entire plan from normalized intake and the exact optional inventory. Tampering
with target fields and rehashing is rejected. Snapshot plans require their original
inventory. Gate JSON contains no purpose text or arbitrary caller metadata.

Checks bind caller repo, Worker, main/protected ref, push/manual event, exact
source SHA and full factory checkout SHA. Unsupported private/sensitive apps,
extra previews/spend, wrong pipeline, missing credential presence and collisions
remain blocked. A reviewed factory allowlist binds exact repo/account alias/Worker/
hostname/plan/source SHA and references owner, scope, expiration, secret selection,
writer exclusivity, domain and budget evidence. The shipped allowlist is empty.
Caller-controlled files cannot replace it. A matching row still cannot prove fresh
provider truth; M2 reports `APPROVAL_REQUIRED` / `PLAN_ONLY`, with publish disabled.
No READY transition or executable deploy exists. This gate models an exact initial
release; routine standing release policy must be designed during authorized M3.

Full factory/workflow pin equality is enforced via documented `job.workflow_sha`
and `job.workflow_repository`, parsed from `toJSON(job)` without printing it.
The actionlint release does not yet recognize these individual new properties;
JSON parsing permits static validation while runtime still fails closed if keys
are absent/mismatched. This GitHub.com contract is unavailable on Enterprise Server.
No hosted runtime compatibility is claimed from local checks.

The reusable workflow accepts `factory_revision`, `plan_path`, optional
`inventory_path`, and `worker`. It serializes by `dev1` + Worker, never cancels
an in-progress gate, and skips untrusted events/unprotected refs before any
secret-presence expression. Caller files resolve inside the checkout; no app
build code executes. Report artifacts expire after seven days. Exit 0 means
a blocked report exists; a skipped job or green run is never release acceptance.

## Future caller (not installed or executed)

```yaml
name: Release readiness
on:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  release-gate:
    uses: kcloud1/cloud-app-factory/.github/workflows/factory-release-gate.yml@<FULL_FACTORY_SHA>
    with:
      factory_revision: <FULL_FACTORY_SHA>
      plan_path: deployment-plan.json
      worker: <EXACT_APPROVED_WORKER>
    secrets:
      CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
      CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

Account ID secret mapping supports existing storage; prefer approved caller variable
`CLOUDFLARE_ACCOUNT_ID` and omit that secret mapping after authorized migration.
Only boolean presence is passed to Python; values are never put into env, logs,
files, output or fingerprints. Presence is not validation. Do not invoke this
example until the protected caller and secret access are approved.

Org owner must select **each exact app caller repository** for the token secret.
Factory selection alone is insufficient. No broad inheritance/selection expansion.
The factory's ordinary `GITHUB_TOKEN` cannot create arbitrary organization repos.
Cloudflare's GitHub App is unnecessary for Actions; native Builds needs its exact
installation/grant and must be disabled for this Actions Worker.

## Readiness evidence and permission separation

Verified: public factory/main/repository identity, admin repository access, merged
M1 schema. Owner reports factory selected for both secrets. Independent org-secret
metadata listing returned 403 on 2026-10-10; no auth refresh or privilege expansion.
Cloudflare scope/expiration/account/domain and live writer state are inaccessible
in this lane. No secret values or provider API calls were made. Those facts are
UNVERIFIED, not passed via synthetic fixtures.

Minimum operation scopes require owner/provider confirmation:

| Operation | Current Cloudflare guidance | Authority |
| --- | --- | --- |
| Existing Worker release without route changes | Editor for the exact Worker | App release approval |
| Create a new Worker | Workers product-level Admin | Separate provisioning authorization; never auto-upgrade recurring deploy token |
| Add/change Custom Domain | Worker Editor plus affected zone Workers Routes Write | Exact hostname/zone authority; confirm effective scope; Custom Domains currently do not support per-Worker roles |
| Repository creation | Approved org GitHub App/token or owner template action | Separate exact repo authority; normal factory GITHUB_TOKEN insufficient |

Existing legacy permissions remain supported; inspect actual permissions rather
than translating a token name into a role. No implied DNS Edit, KV, R2, Secrets
Store, account/global Admin or global API key. First provision can stay an owner
action while recurring releases use restricted credentials.

## Failure and handoff

Invalid schema/digest/path exits 2 with sanitized output. Missing approvals,
metadata or mismatched targets produce blocked reports. A failed/uncertain future
run must reconcile the original run ID and exact target before any retry;
never provision replacements or add a second writer. No deploy retry exists in M2.
Owner approvals and current provider readbacks are required to promote beyond this
gate in a separate reviewed change. [The proposed pilot packet](M3_PILOT_PACKET.md)
is ready for Issue #3; names are proposals, not reservations or authority.

Sources: [GitHub workflow contexts](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts),
[reusable secret context](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows),
[Cloudflare operation permissions](https://developers.cloudflare.com/workers/authorization/workers/),
[Cloudflare Actions integration](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/).
