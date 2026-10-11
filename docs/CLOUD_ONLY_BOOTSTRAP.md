# Cloud-only app bootstrap — PLAN_ONLY handoff

**Owning Issues:** completed [#4](https://github.com/kcloud1/cloud-app-factory/issues/4); source-only adoption review [#14](https://github.com/kcloud1/cloud-app-factory/issues/14).
**Status:** M3/M4 prove two releases of the same factory-pilot. Onboarding prepares proposals; the reviewed publisher remains restricted to that pilot. A second live application is not proven or authorized by this handoff.

## The mobile/Codex Cloud path

1. On GitHub web/mobile, open **kcloud1/cloud-app-factory → Actions → New cloud app — four answers (plan only) → Run workflow**. Enter app name, public fictional purpose, desired exact hostname (or blank to derive), and `$0` budget.
2. Download the `cloud-app-bootstrap` artifact. It includes plan.json, versioned request.json and REQUEST.md, EVIDENCE.json, CODEX_CLOUD_GO.md, public .factory/intake.json, and a read-only factory-plan.yml caller. Hidden files are included after exact bundle validation. No GitHub secret is used by this workflow.
3. After accepting the application's exact intent, the **first owner action** is to create or authorize the exact proposed public `kcloud1/<app>` repository, or reconcile ownership if it already exists. The packet does not create it. Adopt the reviewed repo-starter snapshot in `request.json`; the current template `main` is not automatically the pinned snapshot.
4. The owner must then grant the existing Codex GitHub connection access to that exact repository and publish or reconcile its repository-bound Codex Cloud environment. Select that *published* environment and submit `CODEX_CLOUD_GO.md` as one task. Existing pilot access does not prove this new binding. A GitHub Actions runner is not itself a Codex Cloud task.
5. The approved pilot uses factory-pilot-publish.yml at d60d213b3fa77510deb29b084b0efa802c7c16a4. New apps cannot use its pilot-only allowlist. Their release adaptation is a **blocked decision** until app-specific intent, protected-main control, caller secret selection/token scope, collision/domain ownership, sole writer, billing and rollback evidence are reviewed under separate authorization. The generated read-only caller cannot deploy. For an authorized future release, verify exact run/SHA, Cloudflare version/HTTPS and two actual browser actions before accepting deployment.

## What is reusable now vs. later

| Piece | Status |
| --- | --- |
| Four-answer deterministic planning and one-paste cloud task | M4 merged and verified; seven-file PLAN_ONLY bundle |
| One centralized GitHub Actions planner | Already present: `.github/workflows/factory-plan.yml` |
| One centralized secure **deployment** workflow for every app | M3 PR #7 is merged, security-reviewed and live-proven for factory-pilot only. Arbitrary new apps are not enabled. |
| One Worker and subdomain per approved app | Intended, needs actual provider authorization |
| One-click new repo and automatic Codex Cloud environment creation | **Not proven** with current GitHub/Codex connections; a GitHub App/installation and one-time environment publishing may be required |

## Credentials and authorization

- `$0` is a monthly incremental budget **target**, not a provider spend cap. `request.json` reports `monthly_budget_target_usd` and `budget_enforcement: UNVERIFIED`; the planner retains `BUDGET_ENFORCEMENT_UNVERIFIED`. No billing enforcement or cost-free operation is proven by the packet. Actual charges/limits and rollback/retention need separate owner/provider evidence before a live write.
- `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` stay in **encrypted GitHub Actions secrets**, never Git or Codex prompts. A callable workflow sees only secrets available to its **caller repository** and explicitly mapped; the factory's secrets are **not automatically inherited**.
- Current `kcloud1` plan limits organization-secret access for private repos. Selecting a newly created public app repository for the org secrets is a one-time per-app owner/admin step, unless a separately approved organization-scoped GitHub App automates that selection. Do **not** set org secrets to All public repositories merely for convenience.
- Creation of organization repositories is **not** granted by the default `GITHUB_TOKEN` in a workflow. There is no evidence that this session can automatically publish new Codex Cloud environments.
- The pilot token was shown with `dev1` and `amitk.life` Worker-route authority. Confirm current scope, expiration, secret selection and single deployment writer through fresh provider readbacks before each initial write. No raw tokens in logs.
- Use **one** deployment writer per Worker: GitHub Actions OR native Cloudflare Builds, never both. No AWS, wildcard DNS or extra charges.

## Future release adaptation — blocked decision

A concrete second approved app may justify a separately reviewed app-bound release adapter. That decision is pending; this source-only work does not generalize the credentialed publisher. Any future caller must use the final reviewed interface at its full merged SHA, with exact app inputs and named caller secrets. Until that separately authorized work is complete, the generated workflow deliberately runs only the dry-run planner.

**Success definition:** An actual Codex Cloud app PR merged to `main` causes exactly one GitHub Actions deployment of the same SHA to the exact approved `app.amitk.life`, with a Cloudflare deployment receipt and two live browser PASS results. One-time account/permission initialization is separate from recurring laptop-free releases.

## Determinism and recovery

The short form proposes PERSONAL/public/fictional/static/$0 defaults; it grants no
public exposure or resource authority. Private/sensitive data or other constraints
use the existing structured four-question `python3 factory.py` intake and review.
Exact requested hosts may be a single subdomain of amitk.life; blank derives the
app slug. Wildcards remain forbidden.

Use `--inventory snapshot.json` to flag repository/Worker/hostname matches for
ownership reconciliation; user-entered/offline inventory never establishes READY.
Repeat identical inputs into the same output directory to preserve the packet.
Changed output requires a new revision directory. No provider operations exist.
`request.json` v2 replaces v1's `monthly_cost_cap_usd` with
`monthly_budget_target_usd` and explicit `budget_enforcement: UNVERIFIED`.
Readers must select the request format by `schema_version` and reject unsupported
versions; a historical v1 budget field does not prove provider spend enforcement.
Keep all historical packets unchanged, including any pre-review v1 packet with
the renamed fields; regenerate into a new revision directory, never overwrite or
relabel them. The canonical `plan.json` remains v1 and the normalized-intent
request ID stays unchanged.

Track the same request ID in EVIDENCE.json. PLAN_ONLY is a proposal;
OWNER_APPROVAL_REQUIRED records absent exact authority; READY requires verified
identity, credentials, collisions, sole writer and owner approval; DEPLOYED_VERIFIED
requires actual release evidence. The generator emits only PLAN_ONLY. Observe
saved run/task IDs before any retry; do not create duplicate resources or writers.
