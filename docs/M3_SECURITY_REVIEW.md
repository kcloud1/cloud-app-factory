# PR #7 security corrections and release authority

Owning issue: https://github.com/kcloud1/cloud-app-factory/issues/3
Existing publisher PR: https://github.com/kcloud1/cloud-app-factory/pull/7
Pilot PR: https://github.com/kcloud1/factory-pilot/pull/1

## Corrected boundaries

- P1 config redirection: reject generated `.wrangler` state before packaging and
  again on the clean runner. Generate the only deploy config from factory constants;
  allow only the exact Worker/domain, static assets and disabled public endpoints.
  Revalidate immediately before `node <trusted-wrangler> deploy --config <exact-file>
  --cwd <artifact-root>`. No implicit config discovery or caller Wrangler executable.
  Re-review also requires `--strict`, preventing unknown dashboard-only settings
  from being overwritten in a noninteractive release.
- P1 credentials: independent build and deploy jobs/runners. The build sees no
  provider secrets. Transfer only seven allowlisted inert static files and canonical
  JSON config via this run's immutable artifact ID. Deploy checks out only pinned
  factory source; install its integrity-locked Wrangler 4.149.0 without scripts
  before credentials. No caller source, npm installation/build or npx after injection.
  Node is pinned to 24.21.0, verified against the official release index.
- P2 writer exclusivity: mandatory fresh read-only token/account/zone/Worker/
  domain/DNS/routes readback just before deploy. An existing Worker must yield its
  actual tag, empty native Builds triggers and empty deploy hooks. A full Worker
  inventory proves an absent Worker has no native writer attachment. Any metadata
  error, malformed/incomplete response, connected trigger/hook or conflict blocks
  before Wrangler. No native pipeline is created, disabled or bypassed automatically.

M2's `factory-release-gate.yml` and empty deployment allowlist remain intact.
The publisher allows only protected-main push from `kcloud1/factory-pilot`, the
reviewed full factory SHA, exact `dev1` account and `factory-pilot.amitk.life`.
No paid binding, AWS, token expansion or wildcard configuration is permitted.

## Credential evidence

Current owner instruction records existing `cloud-app-factory` token UI summary:
dev1 Workers Admin/Scripts Edit, nested amitk.life Routes Edit; extra Secrets Store,
DNS Settings and Builds Configuration permissions are unchanged, not widened.
Owner confirmed in this conversation: start October 10, 2026, expiry October 10,
2033; saved token edits and both org secrets selected for the two exact repositories
named in the question (`kcloud1/cloud-app-factory`, `kcloud1/factory-pilot`). These
are owner-confirmed metadata, not independent API policy inspection.

Org-secret metadata API remains 403. Pilot repository-local secret metadata is
readable and empty, which does not disprove inherited org secrets. Local installed
Wrangler 4.149.0 reports unauthenticated; CLI presence is not authentication or
proof of separate Actions permissions. No credential values were accessed locally.
The Actions preflight verifies its actual supplied token is active/not expired,
the approved account/zone is readable, inventory/exclusivity is current and exact.
It must block before write on missing access. Runtime success is still required
and never inferred from owner metadata, test fixtures or a merge.

## Verification and retained state

Focused standard-library guards cover target/config redirects, wrong SHA,
extra executable assets, symlinks and unavailable/connected native Builds.
Existing M1/M2 tests remain unchanged. Actions lint, embedded-shell syntax and a
trusted-tool dry-run use no provider secrets and create no provider resources.
Exact tested HEAD and results are recorded in PR/Issue comments.

Keep the original PRs/Worker/run IDs. Failures are diagnosed on the same attempt;
no manual deploy, replacement resource or blind retry. Only after factory review
PASS may its actual merge SHA replace both pilot workflow pins. Only a successful
Git-triggered deployment plus independent version/HTTPS/source-SHA and exactly two
live browser checks can close Issue #3. M4 waits for that proof.

References: [explicit Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/),
[native Builds trigger API and Worker tag](https://developers.cloudflare.com/api/resources/workers_builds/subresources/triggers/methods/list/),
[Worker script metadata](https://developers.cloudflare.com/api/resources/workers/subresources/scripts/methods/list/),
[token status/validity](https://developers.cloudflare.com/api/resources/user/subresources/tokens/methods/verify/).
