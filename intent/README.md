# Intent Workflow

Use this directory for durable intent records when a meaningful project or change needs more context than the owning GitHub Issue/PR can hold cleanly.

Do not create intent files for tiny/local fixes that satisfy the skip rule in `AI_NATIVE_SDLC.md`.

## Interview Protocol

The agent should help the originator think clearly without turning the interaction into paperwork.

1. **Inspect first** — read the current repository, Issue/PR, and relevant runtime/environment truth before asking questions.
2. **Ask only unresolved material questions** — normally one question at a time.
3. **Challenge selectively** — question assumptions only when they could change scope, architecture, safety, acceptance, or reproducibility.
4. **Use Research / Discovery conditionally** — research outside-in uncertainty; discover inside-out current-state uncertainty.
5. **Preserve nuance** — keep the originator's important words and distinguish verified facts from assumptions.
6. **Restate before acceptance** — summarize the proposed intent and invite correction.
7. **Require explicit originator acceptance** — the agent cannot self-approve intent.

Intent acceptance is not execution authority. Existing `SPEC.md`, user instructions, environment approvals, and safety gates still control mutation.

## Intent Status

Use only these states:

- `DRAFT` — still being clarified.
- `READY_FOR_REVIEW` — agent believes the intent is coherent and has restated it to the originator.
- `ACCEPTED` — explicit originator acceptance exists in the owning conversation or GitHub record.

When setting `ACCEPTED`, record a short acceptance reference or note. Do not infer acceptance merely because the agent finished writing the file.

## First Project Intent

A meaningful new repository normally starts with:

```text
intent/0001-project-bootstrap/intent.md
```

Create it during `INIT.md` initialization. Do not pre-create an empty file in the template.

## Intent Record

Keep the record concise. Include only sections that carry durable decision value.

```markdown
# Intent: <short name>

Status: DRAFT
Owner: <originator>
Owning issue/PR: <link or N/A>
Acceptance evidence: <link/note or pending>

## Originator words
<important original wording or concise faithful summary>

## Problem / Why now
<problem and motivation>

## Desired outcome
<what should be true when this succeeds>

## Users / Operators
<who uses, operates, reviews, or benefits>

## Current state
<verified repository/runtime/environment truth>

## In scope
<included outcomes>

## Out of scope
<explicit non-goals>

## Constraints
<environment, technology, time, cost, data, security, publication, approvals>

## Verified facts
<facts established by repository/runtime/research/discovery>

## Assumptions / Open questions
<remaining uncertainty that matters>

## Success evidence
<what proves the result works and is repeatable>

## Safety / Authority / Cleanup
<mutation boundaries, approvals, rollback, cleanup, retention>
```

## After Acceptance

After intent is accepted:

1. derive a change-specific `spec.md` only when durable requirements/interfaces/acceptance need it;
2. derive `plan.md` only when sequencing, dependencies, rollback, or operational complexity need it;
3. implement against the accepted intent and governing contracts;
4. review the result against the acceptance evidence, not against whatever was easiest to build.

If implementation reveals a material change to the desired outcome or boundaries, update/re-review the intent instead of silently drifting.
