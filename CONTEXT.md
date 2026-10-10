# Context

## Project identity

- Primary repository: https://github.com/kcloud1/cloud-app-factory
- Directory: `/home/user/git/cloud-app-factory`
- Template/reference repositories are read-only.

## Current truth/active work

- Initialized for offline M0–M1; accepted intent and ACTIVE SPEC recorded.
- Issue: https://github.com/kcloud1/cloud-app-factory/issues/1
- PR: https://github.com/kcloud1/cloud-app-factory/pull/5 (M0–M1 delivery).
- Queued follow-up: Issue #2 release gate; #3 needs exact pilot approval;
  #4 depends on #3 live acceptance.
- Amit authorizes Codex review/merge of M0–M1; M2 stays gated.
- No provider resources, deployments or secret reads.
- No M0–M1 runtime blocker; future credentials/domains/resources unverified.

## Next action

Merge validated PR #5, then implement Issue #2's no-write release gate.
