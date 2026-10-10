# Native Codex CLI cloud tasks, independently of VPN

Sources checked: 2026-10-11 (Asia/Singapore).
Issue: [#9](https://github.com/kcloud1/cloud-app-factory/issues/9).

An authenticated personal Codex CLI can submit and inspect cloud tasks using
native **experimental** `codex cloud` commands. Its HTTPS account/task API is
separate from the environment's Tailscale VPN. A laptop running these commands
does not host the cloud task and need not stay on after successful submission.
The same accessible cloud task can be followed in web/mobile. The default
GitHub/Actions/Cloudflare workflow needs neither a local CLI nor a VPN.

```text
Local Codex CLI ──authenticated HTTPS──> Codex cloud task API
                                       └─> task in selected cloud environment

Optional task service request ──Codex proxy──> Tailscale ──> private service
```

## Commands and prerequisites

Use your own normal Codex account sign-in with the intended workspace access.
API-key-only or injected agent authentication does not establish access to cloud
task APIs. Never copy cloud runtime tokens into a personal CLI. The environment
must be available to that account, contain the correct repository, and have its
setup published. GitHub access alone does not prove this binding.

Check the installed version first; cloud commands and flags can change:

```sh
codex --version
codex cloud --help
codex cloud exec --help
codex cloud list --help
```

From the intended local repository checkout, use these Bash examples. Replace
the quoted environment/task placeholders with identifiers actually shown by
your account; do not guess IDs from repository names.

```sh
codex cloud                         # Interactive cloud picker / environment options
codex cloud list --limit 5 --json    # Read-only recent tasks

# Submit only an approved task; submission starts cloud work and uses account quota.
codex cloud exec --env 'ENV_ID' --branch main --attempts 1 \
  'In kcloud1/cloud-app-factory, review Issue #9 documentation only. No VPN or provider changes.'

codex cloud status 'TASK_ID'
codex cloud diff 'TASK_ID'           # Inspect generated changes
```

Use the returned task ID/URL, then inspect the status and final evidence. A
successful submission is not a successful task, tested change or deployment.
`--env` for `list` filters existing tasks; it is required for `exec`. This CLI
version supports `--branch`; specify an existing remote branch rather than
assume a local-only branch is available. `--attempts 1` avoids unnecessary
parallel attempts. Do not resubmit uncertain work blindly and create two writers.

To bring changes to a local checkout, review its status and the diff first:

```sh
git status --short
codex cloud diff 'TASK_ID'
# Only when the local working tree is ready for these reviewed changes:
codex cloud apply 'TASK_ID'
```

`apply` mutates the local working tree. It does not merge a PR, update all
sessions, synchronize files continuously or deploy the app. Preserve local
changes and resolve conflicts deliberately; use GitHub commits/PRs/Issues as
the durable handoff. Normal `codex`/`codex exec` runs locally unless a supported
cloud action is explicitly selected. A resumed local thread is not the cloud VM.

Native commands offer task operations, not an inbound SSH shell, Tailscale SSH,
interactive cloud VM attachment, arbitrary process control or automatic local
filesystem access. Do not describe them as full VM administration. Environment
publishing and repository/account authorization remain separate product controls.

## Validation here and troubleshooting

The managed cloud machine has `codex-cli 0.159.2`. Its help exposes `cloud exec`,
`list`, `status`, `diff`, `apply`; `exec` includes `--env`, `--branch`, `--attempts`;
`list` includes `--limit`, `--env`, `--cursor`, `--json`. This verifies command
availability, not an authenticated personal-computer workflow.

One read-only `codex cloud list --limit 1 --json` attempt returned **HTTP 401**:
the task API could not parse this managed session's authentication token. No
login changes, task submissions, local diff applications or VPN changes were
made. End-to-end local submission/listing remains **UNVERIFIED**. The historical
M4 receipt proves cloud execution through the existing environment, not that
this CLI identity can control it.

| Symptom | Meaning and next step |
| --- | --- |
| `cloud` missing or flag rejected | Check version/help and use a supported CLI; no VPN change needed |
| 401 / sign-in error | On your personal machine, verify normal account sign-in and workspace; do not extract managed runtime credentials |
| Environment missing or GitHub `@codex` asks for one | Verify repository grant, intended account/workspace and published binding; an existing Cloud chat does not prove GitHub integration binding |
| Submission fails | Preserve actual nonzero exit/error and diagnose account/environment access; no task success claim |
| Submission succeeds but task fails | Inspect task evidence; distinguish setup, repository tests and private-service errors |
| Local apply conflicts | Preserve local work, inspect the diff, reconcile in the intended checkout; VPN is unrelated |

Cloud access is subject to account/workspace availability and usage limits.
Existing web/mobile access remains useful if local CLI authentication is
unavailable. No owner action is required to keep the current cloud-only pipeline.

Sources: [official developer commands](https://learn.chatgpt.com/docs/developer-commands),
[cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments),
installed CLI help, and the [M4 cloud receipt](https://github.com/kcloud1/cloud-app-factory/issues/4#issuecomment-6099912560).
For network internals and a separately approved private-service pilot, see
[Codex Cloud + Tailscale](CODEX_CLOUD_TAILSCALE.md).
