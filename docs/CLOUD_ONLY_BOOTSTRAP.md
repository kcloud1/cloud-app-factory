# Cloud-only app bootstrap — M4 staging

**Owning Issue:** [#4](https://github.com/kcloud1/cloud-app-factory/issues/4)
**Status:** Plan/hand-off implementation is ready for review. Deployment is still **gated by the live M3 pilot** ([#3](https://github.com/kcloud1/cloud-app-factory/issues/3)). This is not a second publisher.

## The mobile/Codex Cloud path

1. On GitHub web/mobile, open **kcloud1/cloud-app-factory → Actions → New cloud app — four answers (plan only) → Run workflow**. Enter app name, public fictional purpose, desired exact hostname (or blank to derive), and `$0` budget.
2. Download the `cloud-app-bootstrap` artifact. It includes a deterministic proposed plan, a one-paste `CODEX_CLOUD_GO.md` handoff, a public `.factory/intake.json`, and a small **read-only** caller for the existing shared `factory-plan.yml`. No GitHub secret is used by this workflow.
3. After accepting the new application's exact repo/Worker/domain and completing any one-time provider grant, open **Codex Cloud** in the browser/mobile app. Select that repository's *published* cloud environment; submit `CODEX_CLOUD_GO.md` as one task. Codex Cloud builds, reviews, and opens a PR. A GitHub Actions runner is not itself a Codex Cloud task.
4. **After M3 proves the secure publisher**, the app repository can call **one shared release workflow pinned to a reviewed full commit SHA**. A protected `main` merge triggers deployment; check exact run/SHA, Cloudflare version/HTTPS and two actual browser actions before closing the app Issue.

## What is reusable now vs. later

| Piece | Status |
| --- | --- |
| Four-answer deterministic planning and one-paste cloud task | Proposed in this M4 PR; read-only |
| One centralized GitHub Actions planner | Already present: `.github/workflows/factory-plan.yml` |
| One centralized secure **deployment** workflow for every app | **Not yet live**. M3 draft PR #7 is **pilot-only** and must pass all security review findings and live proof before being generalized. |
| One Worker and subdomain per approved app | Intended, needs actual provider authorization |
| One-click new repo and automatic Codex Cloud environment creation | **Not proven** with current GitHub/Codex connections; a GitHub App/installation and one-time environment publishing may be required |

## Credentials and authorization

- `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` stay in **encrypted GitHub Actions secrets**, never Git or Codex prompts. A callable workflow sees only secrets available to its **caller repository** and explicitly mapped; the factory's secrets are **not automatically inherited**.
- Current `kcloud1` plan limits organization-secret access for private repos. Selecting a newly created public app repository for the org secrets is a one-time per-app owner/admin step, unless a separately approved organization-scoped GitHub App automates that selection. Do **not** set org secrets to All public repositories merely for convenience.
- Creation of organization repositories is **not** granted by the default `GITHUB_TOKEN` in a workflow. There is no evidence that this session can automatically publish new Codex Cloud environments.
- The pilot token was shown with `dev1` and `amitk.life` Worker-route authority. Confirm current scope, expiration, secret selection and single deployment writer through fresh provider readbacks before each initial write. No raw tokens in logs.
- Use **one** deployment writer per Worker: GitHub Actions OR native Cloudflare Builds, never both. No AWS, wildcard DNS or extra charges.

## When the secure shared deployment workflow is ready

Future apps should use a tiny repository-local `push: main` caller that references `kcloud1/cloud-app-factory/.github/workflows/<reviewed-shared-publisher>.yml@<FULL_MERGED_SHA>`, with exact app inputs and **named** caller secrets. Codex must generate this caller from the final reviewed interface—not from a guessed branch or draft PR. Until then, the generated workflow deliberately runs only the dry-run planner.

**Success definition:** An actual Codex Cloud app PR merged to `main` causes exactly one GitHub Actions deployment of the same SHA to the exact approved `app.amitk.life`, with a Cloudflare deployment receipt and two live browser PASS results. One-time account/permission initialization is separate from recurring laptop-free releases.
