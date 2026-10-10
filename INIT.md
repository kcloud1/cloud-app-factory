# Initialization

Status: NOT_INITIALIZED

Use this file only for first-time repository setup or when Amit explicitly asks to reinitialize the project.

## First-Intent Bootstrap

A new meaningful repository starts with one durable project intent before significant implementation.

Do not turn this into a long questionnaire. Inspect repository/runtime truth first, then ask only what is materially unknown, normally **one question at a time**. Challenge an assumption only when it could change scope, architecture, safety, acceptance, or reproducibility.

Cover these areas only as needed:

1. What problem, product, learning goal, or operational outcome does this repository own?
2. Who will use, operate, review, or benefit from it?
3. What does success look like, including the first useful demo or milestone?
4. What already exists: code, repository, runtime, AWS resources, Docker environment, manual process, or prior proof?
5. What is in scope and explicitly out of scope?
6. What constraints matter: PERSONAL/WORK, environment, cost, time, technology, data, publication, security, or approvals?
7. What assumptions or open questions could materially change the direction?
8. What evidence would prove the result works repeatedly?
9. What mutation, rollback, cleanup, or retention boundaries matter?

Preserve the originator's words where they carry useful nuance. Distinguish verified facts from assumptions.

## Research / Discovery Gate

Before finalizing intent, ask whether unresolved uncertainty could materially change the desired outcome, constraints, architecture, or acceptance.

- **Research** is outside-in: current capabilities, official patterns, alternatives, constraints, and reusable solutions.
- **Discovery** is inside-out: actual repository/runtime/environment truth such as topology, versions, configuration, integrations, and dependencies.
- Do only the minimum useful investigation.
- Feed findings back into the intent; do not create a parallel authority source.
- Skip this gate when the technology and current state are already sufficiently known.
- Do not create mandatory research/discovery files; preserve only findings with continuing value.

## Record And Accept Intent

For a meaningful new repository, create:

```text
intent/0001-project-bootstrap/intent.md
```

using the format and interview protocol in `intent/README.md`.

Then:

1. restate the proposed intent to the originator;
2. let the originator correct missing or wrong assumptions;
3. keep the record `DRAFT` until explicit originator acceptance exists;
4. only after that acceptance, record `Status: ACCEPTED` and the evidence/link for the acceptance.

An agent cannot self-approve intent. Intent acceptance confirms the desired outcome and boundaries; it does **not** authorize cloud, PROD, IAM, network, destructive, sensitive-data, or other mutation.

Read-only inspection, Research / Discovery, and repository-initialization documentation may occur before intent acceptance. Significant implementation waits for the accepted intent.

## Initialize Repository Contracts

After the first intent is accepted, update only the files that need project-specific truth:

- `README.md` — purpose and start-here guidance
- `CONTEXT.md` — repository identity, current truth, active work
- `SPEC.md` — execution authority, scope, milestones, stop gates
- `ENV.md` — project runtime/tool/cloud dependencies
- `ROADMAP.md` — only useful future milestones

Derive a change-specific spec or plan only when the proportional artifact rules in `AI_NATIVE_SDLC.md` require them.

Then set this file to:

`Status: INITIALIZED`

Do not repeat this bootstrap for normal future work. Meaningful later changes use the Intent Gate in `AGENTS.md`; tiny/local fixes may use the owning Issue/PR when they satisfy the skip rule.
