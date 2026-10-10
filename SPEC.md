# Specification

Status: DRAFT
Context: `<PERSONAL | WORK>`
Environment: `<LOCAL | LAB | DEV | NONPROD | PROD>`

## Objective

Describe the problem and intended result.

## Outcome

Describe the usable milestone/release package to deliver.

## Authorized

List the actions that may proceed without repeated approval while this SPEC is ACTIVE and the owning Issue/instruction remains in scope.

For `PERSONAL` + `LAB`/`DEV`, explicitly authorized deterministic work may include repo-owned implementation, deployment, cloud resource creation/mutation, validation, reset, and cleanup without asking resource-by-resource.

For `WORK` and especially `PROD`, grant only the bounded authority actually intended. Read-only investigation may be standing authority when explicitly stated; mutation requires proportionate approval in this SPEC or the current user instruction.

Repository visibility is not an authority signal. Private does not mean personal; public does not mean unrestricted.

## MUST

- List required behavior and acceptance-critical invariants.

## MUST NOT

- List hard scope, security, data, publication, production, destructive, or cost boundaries.

## Phases / Milestones

Group related work into a cohesive useful package, normally several tightly coupled tasks or 2-3 phases sharing one outcome and trust boundary.

- Phase 1: `<outcome>`
- Phase 2: `<outcome>`
- Phase 3: `<outcome>`

Do not stop between routine approved phases merely to request permission again.

## Verification

State the smallest meaningful proof: focused tests/checks, runtime/provider readback, user-path validation, and cleanup/retention state when applicable.

## Stop Gates

Stop and ask only when required by a real boundary, for example:

- target repository/account/environment does not match the approved scope;
- work would enter PROD or another higher-risk environment without authority;
- destructive/non-recoverable data loss, credential/secret mutation, public exposure, or material cost is not explicitly approved;
- implementation would materially widen architecture, security/trust boundary, or external integration beyond the milestone;
- required validation fails or current state is ambiguous/unsafe.

Technical failure remains a blocker even when mutation is otherwise authorized.

## Acceptance

List concise conditions that make the whole milestone reviewable and complete.
