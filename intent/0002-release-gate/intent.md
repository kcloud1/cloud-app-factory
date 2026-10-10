# Intent: no-write release gate

Status: ACCEPTED
Owner: Amit
Owning issue: https://github.com/kcloud1/cloud-app-factory/issues/2
Acceptance evidence: Amit's 2026-10-10 instruction to continue, review and merge
the next queued Issues/PRs, combined with Issue #2's explicit no-write scope.
M3 pilot authorization remains separate; no live authority inferred.

## Desired outcome

Extend merged M1 rather than replace it. Choose per-app Actions callers, pinned
to full factory SHAs and using explicitly selected caller credentials. Produce
reviewable exact-target/hash/ref/commit/metadata gates and one M3 owner packet.

## Discovery and constraints

M1 PR #5 merged at `05e5d1408245d74c34d9d913ea86db0dbe10e5f3`.
Public origin and repo admin rights confirmed. Org-secret metadata API returns
403; no permission expansion. No authorized Cloudflare UI/API exists in this lane.
Provider scope/expiration/selection remain unverified and are recorded as gates.

Use Python standard library and existing M1 schema. One PR, no provider write,
deploy run, repo creation, token/secret change, new framework or reference-repo edit.

## Success and plan

Reviewed no-write checker/workflow, exact allowlist and canonical plan validation,
negative boundary tests, safe metadata report and proposed pilot packet. Never
emit READY or enable publication even with synthetic matching approval rows.
Implement → local validation/review → evidence PR → merge → Issue #3 owner gate.
Rollback is source revert; no runtime state exists to clean up.
