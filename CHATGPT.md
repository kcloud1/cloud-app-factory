# ChatGPT-Codex Repository Adapter

Purpose: keep only repository-specific ChatGPT/Codex coordination details here while reusable policy remains canonical in Agent OS.

Canonical reusable guidance:

- Collaboration protocol: https://github.com/amitkarpe/agent-os/blob/main/kb/playbooks/integrations/chatgpt-codex-collaboration-protocol.md
- Connector Safety Gate: https://github.com/amitkarpe/agent-os/blob/main/kb/policies/connector-safety-gate.md
- Portfolio Economy Defaults: https://github.com/amitkarpe/agent-os/blob/main/AGENTS.md#portfolio-economy-defaults

This file is an adapter/router, not a second copy of those policies. Repository-specific rules and authority still remain local.

## Default Behavior

When the current objective is known, `go`, `g`, `.`, `Y`, `yes`, or equivalent affirmative continuation means: fetch current durable GitHub state and execute the approved objective within existing authority and constraints.

Do not start another planning round unless Amit explicitly asks for `plan`, `review`, `discuss`, or a decision. Stop only for a real safety, scope, authorization, repository-identity, access, or validation blocker.

Amit is the decision-maker, not the copy/paste transport layer. ChatGPT and Codex should fetch the owning Issue, PR, comments, current HEAD, and relevant validation themselves when accessible.

## Short Actor Names

For fast dictation and handoffs:

- `G` = ChatGPT.
- `X` = Codex.

Interpret these by sentence role, not capitalization alone. A standalone `g` remains the `go` continuation command; `G/g` used as an actor in a phrase means ChatGPT, for example `ask G to merge`. `X/x` used as an actor means Codex, for example `X must test`.

Actor aliases are shorthand only. They never widen scope, execution authority, merge permission, or safety gates.

Generic G/X role definitions, direct/delegated execution rules, handoff behavior, context-loading economy, milestone sizing, and validation economy follow the canonical Agent OS collaboration protocol above.

## Repository Binding Guard

`CONTEXT.md` records the Primary Repository and optional Authorized Related Repositories when recovery state needs to preserve those bindings.

Before a write, mutation, PR action, or implementation:

1. resolve the repository that owns the current objective;
2. compare it with the Primary Repository and any explicitly authorized related repositories when those bindings are recorded;
3. confirm that the current Issue/PR belongs to that objective.

Reading or researching other repositories is allowed. Cross-repo writes are allowed when Amit explicitly requests them or the active SPEC/Issue clearly requires them.

If a short continuation such as `go` or `Y` points to an unrelated repository and intent is not explicit, stop with `BLOCKED_REPO_MISMATCH` and ask one short confirmation. Never bypass this guard merely because the referenced PR is the newest one.

## Optional Session Binding

Session metadata is useful coordination context, not authority. Populate it only when discoverable; never guess values or create Git churn only because a session identifier changed.

Codex may record:

- Directory: `~/git/<repo>`
- Thread name: `<repo or task>`
- Session: `<Codex session UUID>`

ChatGPT may record when available:

- Project: `<optional>`
- Chat name: `<optional>`
- Session ID or URL: `<optional>`

Repository identity, the applicable SPEC/Issue, and Amit's current instruction remain authoritative when session metadata is stale or absent.

## Local Context And Handoff Rules

`AGENTS.md` owns the repository read contract. For warm continuation, use the owning Issue/PR, latest relevant authorized delta, current HEAD/diff, and only the governing files relevant to the task.

`CONTEXT.md` is current-only recovery state, not the normal execution packet and not project history.

Use the existing owning PR for implementation/review corrections; if no PR exists, use the owning Issue. Do not create packet/outbox files for state already recorded in GitHub.

When a manual copy/paste handoff is genuinely required, keep it self-contained and point back to the durable owning Issue/PR. The reusable handoff and direct G -> X/Factory rules are owned by the canonical Agent OS collaboration protocol.

## Local Execution Authority

`SPEC.md` is the repository execution/authority contract when the work requires one. An ACTIVE SPEC/Issue may grant standing authority for explicitly bounded work.

Do not infer authority from repository visibility. A private repository may be personal or work; a public repository may still have strict mutation boundaries.

Explicit no-merge, production, destructive, credential, public-exposure, publication, security, and other applicable gates remain binding. Technical failures remain blockers even when mutation is otherwise authorized.

Never publish credentials, tokens, private keys, customer data, or raw sensitive infrastructure details.

## Connector Safety Gate

Connector/platform actions follow the canonical Agent OS Connector Safety Gate linked above.

Repository-specific exceptions may narrow that policy but must not silently weaken or bypass it.
