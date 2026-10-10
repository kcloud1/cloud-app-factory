# Small release acceptance receipt

Paste one receipt into the owning Issue/PR; keep credential values and sensitive
account details out. This is reusable evidence guidance, not another approval gate.
For another provider, use its equivalent event/build/deployment identifiers and
record any unavailable field rather than inventing it.

```text
Repository / PR:
Accepted authority / environment / owner onboarding reference:
Delivery mode: native Git build | manual snapshot | blocked
Production branch / exact merged commit SHA:
Provider build ID / trigger event / source commit SHA:
Build result / timestamp / log or dashboard link:
Deployment ID / active version / traffic / link:
Worker or app identity / approved custom hostname:
Custom-domain HTTPS result / visible release marker / observation time:
Source parity: checked-in config and public assets match the build source
Live check 1: <primary interaction and expected visible result> — PASS/FAIL
Live check 2: <second relevant interaction and expected result> — PASS/FAIL
Credential scope confirmation: owner/provider evidence reference, never a value
Retained resources / cost boundary / blocker / recovery or next action:
```

## Acceptance checklist

- [ ] Record the **full merged SHA**, not only the PR head. The native build's source
  SHA must match exactly and its trigger must be **`push_event`** for Cloudflare's
  Git push proof. Connecting a repo, retrying a build or invoking a deploy hook is
  different evidence; label it honestly and prove a subsequent authorized push.
- [ ] Build completed successfully. Record its ID/log link and the active deployment
  ID/version/traffic; `source: wrangler` alone does not distinguish a developer upload
  from Wrangler running inside native Builds. Correlate it to the push build.
- [ ] Verify the **custom-domain HTTPS** page and its public assets load, the expected
  marker is visible, and the binding still targets the intended app after deployment.
  A workers.dev check alone is not custom-host acceptance; certificate/DNS readback
  alone is not a live browser result.
- [ ] Run **exactly two app-relevant live browser interactions**, preferably on the
  custom hostname, with expected/actual results in the receipt. For the optional
  starter: (1) marker plus Try the demo updates status with no cloud action;
  (2) dark/light toggle changes the theme and remains usable on a narrow viewport.
  Replace these with the finished app's useful flows; no new test framework is required.
- [ ] Record Git versus manual truth, verified scope reference, cost/retention and any
  gaps. Close the owning Issue only when its full acceptance is met. Do not promote
  previous manual snapshot evidence into an automatic release claim.

## Recovery without a second pipeline

Missing GitHub grant, Builds config or unreadable credential scope: leave a ready PR
unmerged, identify the exact owner UI/permission action, and retain the current live
version. Once resolved, use the same PR/authorized merge to trigger native Builds.

Failed build: capture build ID, exact SHA and the failing step; fix the same cohesive
PR if unmerged, or a focused corrective PR after merge. A manual retry must be labeled
as such; it does not prove the original push succeeded. Do not add an Actions pipeline,
new token or replacement Worker to bypass the failure.

Wrong version/domain or failed live check: stop completion claims, preserve evidence,
and use an owner-authorized rollback to a known good version or source revert followed
by the native Git build. Record rollback IDs and source parity. DNS changes and disabling
builds still need their applicable authority. No blind repeated uploads or wildcard DNS.

## Proven reference and its limits

[Level 4 completion](https://github.com/kcloud1/cloud-ops-demo/issues/5#issuecomment-6094650672)
records merged SHA `d0e61e0037b7841cb27a40758c0bd3f93c2e9095`, native `push_event`
build `f2fad67a-b2db-4c19-8ed3-f02d32744fa5`, deployment
`b261f2c2-d832-40e4-8630-5b39a8dd2767`, and active version
`a20bd8c4-a9f9-44ed-9c4b-ab2c2c3af6fe`, plus two live workers.dev interactions.
The [custom hostname](https://cloud-ops.amitk.life/) had separate binding/HTTPS fetch
evidence; the receipt does not claim its two browser interactions ran there.
The selected credential deployed successfully but full scope was unreadable. New
projects must confirm scope before reuse. Reuse this evidence; do not repeat that
app's tests or deploy another Worker to validate the template.
