# <Project Name>

One sentence explaining the problem this repository solves.

## Start Here

For agents, `AGENTS.md` is the single read router. It defines the cold-start/recovery order and when other repository contracts must be loaded.

For current work, prefer the owning GitHub Issue/PR and current HEAD. Load the other root files only for the responsibility they own:

- `AI_NATIVE_SDLC.md` — proportional Intent -> Spec -> Plan -> Code/Test/Review lifecycle
- `intent/README.md` — reusable Intent Gate, interview, acceptance, and first-intent record protocol
- `CONTEXT.md` — current-only recovery state when restart/current-state context is needed
- `SPEC.md` — execution authority and milestone contract when implementation, mutation, deployment, cleanup, or safety boundaries matter
- `ENV.md` — project runtime/tool/cloud dependencies when environment facts matter
- `CHATGPT.md` — repository-specific ChatGPT/Codex adapter, shorthand, and repository-binding guard
- `INIT.md` — one-time initialization only
- `ROADMAP.md` — useful future direction, not current authority

For optional laptop-free deployment of a Codex Cloud app, see [Cloud-first quickstart](docs/CLOUD_FIRST_QUICKSTART.md). It is a reference workflow, not an extra approval or bootstrap gate.

Cloudflare is an opt-in path: [six-file static starter](examples/cloudflare-static/README.md),
[owner onboarding and new-project checklist](docs/CLOUDFLARE_WORKERS_ONBOARDING.md),
and [release evidence / recovery receipt](docs/DEPLOYMENT_EVIDENCE.md). The template
provisions nothing and carries no provider credentials or active root deployment config.
Complete `INIT.md` first; the owner's `<app-name>.amitk.life` convention is optional
for other owners. Use native Git Builds only after the one owner integration gate.

Do not use this README as a second copy of the agent bootstrap policy.

## Template Model

Keep root contracts separate by responsibility:

- `AGENTS.md` — universal agent entry/router and local repository rules
- `CHATGPT.md` — thin repository-specific ChatGPT/Codex adapter
- `CONTEXT.md` — current-only project/repository recovery state
- `SPEC.md` — execution authority and milestone contract when needed
- `INIT.md` — one-time first-intent bootstrap for a new repository
- `ENV.md` — project runtime/tool/cloud dependencies when needed
- `ROADMAP.md` — useful future milestones, not current authority

Historical detail belongs in Git history, closed Issues/PRs, or `docs/history/` when needed — not in `CONTEXT.md`.

Reusable cross-project policy belongs in Agent OS and should normally be referenced rather than recopied here. Machine-specific facts belong in the active `~/.agent/HOST.md` when available.

Preserve useful local knowledge. Context-loading economy means reading the right file at the right time, not deleting information.
