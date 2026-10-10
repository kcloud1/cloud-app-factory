# AI-Native SDLC v1

Status: v1 (effective on merge)  
Applies to: repositories created from `repo-starter`

## Principle

Use the AI-native lifecycle:

```text
Intent -> Spec -> Plan -> Code -> Tests/Evals -> PR/Review -> Deploy -> Observe -> New Intent
```

Human input should stay focused on outcome, constraints, approval boundaries, and meaningful review. AI should derive detailed requirements, implementation plans, code, tests, documentation, and evidence. Keep the process proportional: artifacts exist to improve correctness, safety, reproducibility, and continuation — not to create ceremony.

## Research / Discovery Gate

Before approving a meaningful Intent, check whether unresolved uncertainty could materially change the desired outcome, constraints, architecture, or acceptance.

- **Research = outside-in** — learn the external technology/solution space: current capabilities, official patterns, alternatives, constraints, and reuse opportunities.
- **Discovery = inside-out** — inspect the actual current repository/runtime/environment: topology, versions, configuration, integrations, dependencies, and operational truth.
- If neither would materially change the Intent, skip the gate and continue.
- If either is needed, do the minimum useful investigation, distinguish verified facts from assumptions, and feed the findings back into the Intent before approval.
- Do not require separate `research.md` or `discovery.md` files. Keep durable findings in the owning Issue/PR or repository documentation only when they have continuing value.

Tiny/local fixes normally skip this gate.

## Intent Gate

Meaningful new work must have one authoritative intent before significant implementation.

The agent should inspect known truth, interview only unresolved material points, challenge assumptions selectively, and restate the proposed intent for correction. Use `intent/README.md` when a separate durable intent record adds value.

The agent may draft or structure the intent, but it cannot self-approve it. Record `Status: ACCEPTED` only after explicit originator acceptance exists in the owning conversation or GitHub record.

Intent acceptance confirms the desired outcome and boundaries. It does **not** grant cloud, PROD, IAM, network, destructive, sensitive-data, or other mutation authority; those remain governed by the repository execution contract and current user/environment approval.

Tiny/local fixes that satisfy the exact skip rule may use a sufficient Issue/PR directly.

## Ten Contracts

1. **Purpose** — `README.md` states why the repository exists, who it serves, and its important non-goals.
2. **Intent** — meaningful work starts from one authoritative intent record: the originator's problem, desired outcome, constraints, assumptions, and open questions, linked to the owning Issue, PR, and revision. The agent may structure it, but explicit originator acceptance is required before it is treated as accepted.
3. **Specification** — AI converts approved intent into reviewable requirements, interfaces, environment assumptions, safety boundaries, and acceptance criteria.
4. **Plan** — before significant implementation, define the change sequence, dependencies, validation, failure handling, rollback, and retained state.
5. **Git is complete** — runtime work on EC2, Docker, AWS, local hosts, or other systems is not complete until the code, IaC, configuration, scripts, and instructions needed to reproduce it are committed.
6. **Deterministic execution** — AI may reason probabilistically, but repeatable build, deploy, validation, remediation, cleanup, and promotion paths should graduate into repo-owned scripts, IaC, CI/CD, or provider-native automation.
7. **Tests and CI** — prove the smallest meaningful acceptance surface, including representative negative/failure cases. CI proves only the configured checks on the exact tested revision; repeatability and runtime acceptance need their own relevant evidence. Test count is not the objective.
8. **Safety and authority** — identity, repository, account, environment, target, permissions, mutation boundary, approval, cost, rollback, and cleanup must be explicit where relevant. Read first, change second; fail closed on uncertainty.
9. **Evidence** — "done" requires revision + relevant tests + runtime/provider readback when state matters + acceptance result + cleanup/retention state. A command success or delivery receipt is not execution or acceptance proof.
10. **Learning** — every meaningful escaped failure asks: "What permanent check would have prevented this?" Add the regression in the project first. After sanitization and owner review, promote reusable lessons to Agent OS or a reusable skill; put only genuinely universal starter defaults in `repo-starter`.

## Artifact Rule

Artifacts are selected by risk and complexity, not task size alone. Intent, specification, and planning information must be sufficient and authoritative; separate files are conditional unless the governing project contract requires them.

| Work type | Intent record / `intent.md` | change `spec.md` | `plan.md` |
|---|---|---|---|
| Tiny/local fix | Owning Issue/PR may suffice | Optional | Optional |
| Meaningful feature or milestone | Durable intent required; use `intent.md` when it adds enduring context beyond a sufficient Issue | Required when requirements/interfaces/acceptance need separate durable review | Required when sequence, dependencies, rollback, or multiple implementation steps need a separate execution record |
| High-risk work: AWS/PROD/IAM/network/security/data/destructive/material-cost/trust-boundary | Durable approved intent required | Approved specification and operating contract required; use an existing equivalent or a change-specific file | Durable reviewed plan required when multi-step, rollback-sensitive, operationally complex, or dependent on external state |

### Exact skip rule

A tiny/local fix may use the owning GitHub Issue/PR as both intent and plan when all of the following are true:

- one bounded outcome;
- no new trust/security boundary;
- no PROD, IAM, network, destructive, sensitive-data, or material-cost change;
- no material architecture/design decision;
- implementation and rollback are obvious;
- acceptance can be expressed directly in the Issue/PR.

For other work, a sufficient owning Issue may hold the required intent, specification, or plan without duplicate files, provided the governing contract permits it. Required information, review, approvals, and governed execution plans cannot be skipped. Keep enduring behavior and intent in versioned project documentation before closing the Issue; link rather than duplicate.

This is a deliberate local adaptation of the source playbook's committed `intent.md` / `spec.md` / `plan.md` model, reconciled with the existing Agent OS sufficient-Issue rule. Never create empty ceremonial files or a second source of authority.

## Change Artifact Layout

When separate change files add value, use:

```text
intent/<change>/
  intent.md    # when required
  spec.md      # when required
  plan.md      # when required
```

`intent.md` preserves the originator's intent; AI may structure it, but must not silently replace the desired outcome.

The change-specific `spec.md` defines what must be true for that change. It does **not** replace the root `SPEC.md`, which remains the repository-level execution, authority, and safety contract.

The change-specific `plan.md` defines how the approved specification will be implemented and proven. It is not a second roadmap.

## Default Execution Loop

```text
Originator's desired outcome
  -> capture draft intent
  -> optional Research / Discovery Gate when uncertainty could change the intent
  -> refine and approve intent
  -> AI derives specification
  -> human reviews outcome + boundaries
  -> AI derives implementation plan
  -> code / IaC / configuration
  -> focused tests and CI
  -> explicitly approved DEV validation when relevant (non-PROD only)
  -> PR review + required checks + merge
  -> applicable environment approval before release/deploy
  -> deploy + provider/readback evidence + acceptance + observe
  -> cleanup / retained-state record
  -> escaped failure becomes a regression or reusable rule
  -> next intent
```

Pre-merge runtime validation is limited to explicitly approved non-PROD targets; it does not authorize release or PROD changes. Release follows applicable review, merge, and environment approval.

For delegated or stateful execution, retain the request digest, exact target identity, execution/run ID, revision, evidence pointer, and terminal outcome in the owning record or an appropriately private evidence store. Reconcile the original execution and current target state before any permitted retry; uncertainty blocks redispatch. A delivery receipt proves admission only; the controller separately verifies acceptance.

Keep public examples generic (DEV / PROD and placeholders). Never publish credentials, authentication state, private repository identifiers, private infrastructure details, or raw sensitive evidence.

GitHub Issue/PR remains the normal workflow, authority, coordination, and evidence plane. Context loading stays event-driven: use the owning Issue/PR, current HEAD/diff, and only the governing files relevant to the task.

## Adoption And Pilot

### New repositories

Use `INIT.md` to turn the originator's rough idea into the first accepted project intent. For meaningful new repositories, create `intent/0001-project-bootstrap/intent.md` during initialization rather than pre-creating an empty template file.

A fresh-repo pilot passes when:

- a rough idea triggers the first-intent bootstrap;
- known repository/runtime facts are inspected before questioning;
- unresolved material questions are asked rather than silently guessed;
- Research / Discovery runs only when it can materially change intent;
- the originator explicitly accepts the intent before significant implementation;
- Spec / Plan are derived proportionally;
- tiny/local fixes can still use the skip rule;
- CI/check success and actual runtime acceptance remain separate evidence.

### Existing repositories

Adopt incrementally. Do not invent historical intent or rewrite repository history merely to fit this model.

For the next meaningful change:

1. start from current Git/GitHub truth;
2. use Discovery when current runtime/environment state could change the work;
3. reconcile important runtime-only implementation back into versioned code/IaC/configuration when needed;
4. preserve existing safety and authority contracts;
5. capture and accept the next meaningful intent, then continue through Spec / Plan proportionally.

An existing-repo pilot passes when current truth is preserved, no historical intent is fabricated, the next meaningful change uses the Intent Gate, and runtime evidence is reconciled separately from CI evidence.

### Useful measurements

Measure only what can improve the process:

- material assumptions found before coding;
- rework caused by missed requirements or environment facts;
- reproducibility from Git, CI, and runtime evidence;
- handoff/restart clarity;
- escaped defects converted into regression checks.

Do not use document count, question count, or test count as productivity measures.

## References

- https://claude.com/blog/the-ai-native-sdlc-playbook
- https://academy.claude.com/courses/ai-native-sdlc-playbook
- https://academy.claude.com/courses/ai-native-sdlc-playbook/capture-intent
- https://academy.claude.com/courses/ai-native-sdlc-playbook/requirements-and-design
- https://academy.claude.com/courses/ai-native-sdlc-playbook/plan-mode
