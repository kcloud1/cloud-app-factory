# Context

## Project identity

- Primary repository: https://github.com/kcloud1/cloud-app-factory
- Directory: `/home/user/git/cloud-app-factory`
- Template/reference repositories are read-only.

## Current truth/active work

- Initialized for offline M0–M1; accepted intent and ACTIVE SPEC recorded.
- Active issue: https://github.com/kcloud1/cloud-app-factory/issues/2
- M0–M1 PR #5 merged; no-write M2 release gate on `feat/2-release-gate`.
- Issue #3 needs exact pilot approval and provider metadata;
  Issue #4 cannot dispatch until #3 live acceptance.
- Amit authorizes Codex review/merge of M0–M1; M2 stays gated.
- No provider resources, deployments or secret reads.
- Org-secret metadata listing denied (403); no authorized Cloudflare readback.
  Future credentials/domains/resources remain unverified; offline gates complete.

## Next action

Publish/review/merge Issue #2 PR, then retain Issue #3's exact pilot owner gate.
