# Specification

Status: ACTIVE
Context: PERSONAL
Environment: LAB (repository/offline planning only)
Owning issue: https://github.com/kcloud1/cloud-app-factory/issues/1
Accepted intent: [bootstrap](intent/0001-project-bootstrap/intent.md)

## Objective and authority

Build a reusable four-answer factory for independently developed/deployed apps.
M0 initializes contracts. M1 delivers deterministic offline intake, inspectable
plans, conflict/authorization gates, an example, focused validation and a reusable
Actions dry-run workflow with future deployment design.

Amit's 2026-10-10 GO authorizes implementation, local checks, branch/commit,
one cohesive PR and Issue evidence. His later explicit instruction authorizes
Codex to review and merge M0–M1 without waiting for G. M2 remains gated.
Follow-up Issues/PRs require their own approved scope; do not invent work to meet a count.

## MUST

- Four top-level answers, strict schema, sanitized invalid-input errors.
- Stable JSON/digest, conservative repository/Worker names, exact DNS hostname.
- Validate privacy choices and finite nonnegative USD budget.
- Flag absent/stale inventory and collisions; never infer ownership from names.
- Always dry-run with execution disabled; missing authority blocks.
- One isolated Worker per app; exactly one deployment pipeline per Worker.
- Workers.dev and previews disabled unless separately approved.
- Explicit credential mapping, no values read/printed, no broad inheritance.
- One cohesive implementation PR, preserving existing governance.

## MUST NOT

Create app repositories, Workers, DNS, tokens, installations, AWS resources,
spending or public apps; execute deploy workflows; widen credentials; modify
`repo-starter` or `cloud-ops-demo`; add unnecessary dependencies/test frameworks.
No live credential test.

## Interface and implementation plan

`factory.py --intake FILE [--inventory FILE] [--mode dry-run]` uses
`examples/intake.json`'s schema. Without a file it asks four questions.
Exit 0: plan produced, not permission. Exit 2: invalid input.
Plans contain target, architecture, normalized intake, conflicts, blockers,
credential contract and future acceptance criteria. Inventory cannot unlock execution.

1. Verify origin/Issue/acceptance and initialize contracts.
2. Implement standard-library planner and reusable dry-run/design.
3. Validate determinism, malformed input, conflicts, privacy and authorization;
   review the actual diff.
4. Publish evidence, review and merge the single PR under updated owner authority.

Local checks do not prove Codex Cloud, secret access, provider permissions,
domains, builds or live apps. Failed validation keeps the same PR for correction.
Rollback is a reviewed source revert; no runtime resources need cleanup.

## Stop gates and acceptance

Stop on identity mismatch, unresolved validation failure or work outside limits.
Pass: complete contracts, working deterministic valid/invalid intake, explicit
unresolved gates, reviewed workflow/design and one evidence-backed PR.
M2 requires the separate [exact authorization packet](docs/FACTORY_PIPELINE.md).
