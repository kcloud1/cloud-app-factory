# Optional AWS Cloud toolkit

Issue [#11](https://github.com/kcloud1/cloud-app-factory/issues/11) authorizes
software setup and credential-free checks only. Default Cloudflare projects need
no AWS tools. This profile never changes existing pipelines or authenticates.

## Select one profile

| Profile | Tools pinned on 2026-10-11 |
| --- | --- |
| `core` | AWS CLI **2.37.12**, GitHub CLI **2.102.0** |
| `cloudops` | core + Session Manager Plugin **1.2.896.0**, Terraform **1.16.5** |
| `app-dev` | core + project-local Amplify Gen 2 backend CLI **1.10.0**, backend **1.25.1** |

Supported base: Linux **glibc**, x86-64 or ARM64, Git, Python >=3.10.
`cloudops` also needs `dpkg-deb` (extraction only). `app-dev` needs existing
Node **22 or 24 LTS** and npm. Unsupported bases stop with a concrete error;
no sudo, OS package install, Node install or global shell edit occurs.

```sh
# Run inside a checkout of the factory at its reviewed, full M6 merge SHA.
python3 scripts/aws_toolkit.py --plan core       # default; no downloads
python3 scripts/aws_toolkit.py --install core    # explicit opt-in
python3 scripts/aws_toolkit.py --check core      # only version inventory

python3 scripts/aws_toolkit.py --install cloudops
python3 scripts/aws_toolkit.py --check cloudops

# Existing authorized app repo; its root package.json remains untouched.
python3 scripts/aws_toolkit.py --install app-dev --project-dir /workspace/my-aws-app
python3 scripts/aws_toolkit.py --check app-dev --project-dir /workspace/my-aws-app
```

`--prefix /path/to/owned/toolkit` overrides the default
`~/.local/share/cloud-app-factory/aws-toolkit`. A mismatched system version is
left intact; the pinned version installs in the isolated prefix. Exact versions
already available are reused. To use managed binaries, add the receipt's
`path_for_this_task` to PATH **for the current task only**. Save that path in the
project handoff; no persistent dotfile edits are needed. Checks exit 1 for missing
or unpinned tools, 2 for invalid/unsupported setup. Plans exit 0 and show gaps.

Each fixed HTTPS archive must match its committed SHA256 before extraction or
execution. ZIP/TAR links and traversal are rejected. AWS uses its bundled CLI
executable; SSM's deb is extracted without running package scripts and only its
client binary is retained. No SSM service is installed or started. Per-prefix
nonblocking locking prevents concurrent installations. Existing managed
collisions fail closed rather than overwrite files. Completed earlier tools may
remain if a later tool fails; inspect the inventory before retrying.

Amplify installs under `<project>/.aws-toolkit/app-dev`, with a committed factory
package/lock copied there and `npm ci --ignore-scripts --no-audit --no-fund`.
Required top-level peers are explicitly pinned: `aws-cdk-lib`
**2.273.0**, `constructs` **10.8.1**, `@aws-sdk/types` **3.974.6**;
`@aws-cdk/toolkit-lib` **1.19.0** and `@opentelemetry/core` **2.0.0** are explicit
to cover bundled dependency entries
that npm otherwise omits from its generated lock. These are local
Amplify dependencies, not separately installed global CDK/SAM commands.
Transitive dependencies are locked and npm verifies lockfile integrity. Never use
`npx ampx` without a local pin: invoke
`npm exec --offline --no -- /absolute/project/.aws-toolkit/app-dev/node_modules/.bin/ampx --version`
for this check. The installer supplies npm context in an empty scratch directory
without resolving a floating package. Actual app
backend dependencies and its provider locks remain per-project. No Gen 1 global
CLI, sandbox, backend scaffold, CDK or SAM is installed by default. Add
`.aws-toolkit/` to that project's `.gitignore`; retain the factory revision and
package-lock digest in the handoff. Do not commit `node_modules`.

Version subprocesses use temporary empty HOME/config paths, a credential-free
environment allowlist, metadata disabled and telemetry disabled. They run only
version commands, outside project infrastructure directories. Neither AWS/SSO
files nor `.env` are read. Checks create disposable scratch directories but do
not download or modify installed/project tooling. No auth, session, Terraform
init/plan or Amplify sandbox command is part of installation or checks.

## Codex Cloud adoption

Use the **existing** repository-bound Cloud environment. Setup scripts can run
these same opt-in commands after checking out the factory at the reviewed full
SHA. Give setup access to the named vendor HTTPS download hosts and npm registry
only as needed; ordinary check-only tasks need no download access. Record the
prefix and re-run `--check` after environment cache resets. Installing here does
not install tools on a laptop or on a GitHub Actions runner.

A complete handoff for one future authorized project:

```text
repository: OWNER/EXACT-AWS-APP
owning_issue: https://github.com/OWNER/EXACT-AWS-APP/issues/NUMBER
factory_revision: FULL_REVIEWED_M6_MERGE_SHA (replace before adoption)
runtime: existing repository-bound Codex Cloud environment
profile: cloudops
prefix: /workspace/tooling/aws-toolkit
setup: python3 /workspace/factory/scripts/aws_toolkit.py --install cloudops --prefix /workspace/tooling/aws-toolkit
check: python3 /workspace/factory/scripts/aws_toolkit.py --check cloudops --prefix /workspace/tooling/aws-toolkit
task_path: /workspace/tooling/aws-toolkit/bin
future_account: 333438771545
future_region: ap-southeast-1
authentication: NONE; requires a separate exact-task approval and trust design
resource_authority: NONE; software-only receipt required
```

Replace repository/Issue/SHA using the future project's accepted intent. For
`app-dev`, include its exact `--project-dir` and package-lock SHA256. Adopt the
compact [aws-cloudops Skill](../.agents/skills/aws-cloudops/SKILL.md) with these
references, rather than copying credentials, IAM grants or SDK trees. Projects
without AWS needs make no changes. Private SSM access additionally needs approved
caller/destination IAM, running SSM agent and VPC connectivity/endpoints; the
plugin alone supplies none of them. M5/Tailscale is optional, never a fallback.

## Authentication design only

Future GitHub Actions deployments should use short-lived AWS OIDC sessions.
Review this **proposed** trust condition on a separately approved role:

```json
{
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
    "token.actions.githubusercontent.com:sub": "repo:OWNER/EXACT-REPO:ref:refs/heads/main"
  }
}
```

For a protected environment, use the exact subject
`repo:OWNER/EXACT-REPO:environment:EXACT-ENVIRONMENT` instead, and enforce main-only
branches plus approvals on that environment. Check the exact AWS account and
provider, repository ownership, protected source, audience, least-privilege role
policy, session duration and readback before enabling `id-token: write` in that
future workflow. No wildcard repositories or branches; review allowed actions
against the exact resource ARNs. M6 creates no provider, role, policy or workflow.

Codex Cloud is a **separate trust boundary**: GitHub's job OIDC token is not
available automatically in a Cloud task. Authentication is unverified here; do
not place long-lived keys in Vault/secrets, share SSO caches or export corporate
credentials. Future separately approved checks must establish caller identity,
exact account and region first. Personal example account `333438771545`,
`ap-southeast-1` is not permission. Official DEV `672172129528`, PROD and other
accounts are excluded unless explicitly named and approved.

## Rollback and validation

No automatic uninstall touches shared software. Review the receipt's absolute
prefix, then remove only its managed symlinks and version directories (or the
entire dedicated prefix if exclusively owned). To roll back, use a previous
reviewed factory SHA and a **new prefix**; existing mismatched managed links
intentionally block installation. Remove only the project's dedicated
`.aws-toolkit/app-dev` to replace an incomplete or reviewed older Amplify install;
its root app files are preserved. Never remove global packages or credentials.

```sh
python3 -m unittest discover -s tests -p 'test_aws_toolkit.py'
python3 scripts/aws_toolkit.py --check cloudops --prefix /tmp/owned-validation-prefix
```

Validate the real install/check twice in a disposable prefix/project. ARM64
artifacts have pinned hashes; runtime acceptance requires an ARM64 runner and is
not inferred from an x86-64 check. This setup proves software availability only.
No authenticated AWS operations or charges are part of M6.

## Research sources

- [AWS CLI Linux installers and custom installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html): versioned x86-64/ARM64 bundles. AWS archive SHA256 values were computed from the exact vendor HTTPS files on 2026-10-11; they are not claimed to be vendor-published checksums.
- [GitHub CLI 2.102.0 release](https://github.com/cli/cli/releases/tag/v2.102.0): release asset digests.
- [SSM plugin Linux](https://docs.aws.amazon.com/systems-manager/latest/userguide/install-plugin-debian-and-ubuntu.html) and [1.2.896.0 release](https://github.com/aws/session-manager-plugin/releases/tag/1.2.896.0): versioned vendor S3 debs; committed SHA256 values computed from those exact files.
- [Terraform installation](https://developer.hashicorp.com/terraform/install), [1.16.5 checksums](https://releases.hashicorp.com/terraform/1.16.5/terraform_1.16.5_SHA256SUMS), [per-project provider locks](https://developer.hashicorp.com/terraform/language/files/dependency-lock).
- [npm ci](https://docs.npmjs.com/cli/v10/commands/npm-ci/): reuse the same peer-resolution flags as lock generation; validation base npm 10.9.8.
- [Node supported releases](https://nodejs.org/en/about/previous-releases): Node 22/24 LTS base; Node 18/20 are EOL.
- [Amplify Gen 2 manual setup](https://docs.amplify.aws/react/start/manual-installation/): project-local backend/CLI, ESM; public npm package metadata supplies exact pins and the lockfile supplies integrity.
- [GitHub AWS OIDC](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws), [AWS OIDC providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html): future trust design only.
- [Codex Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments): repository-bound setup/cache model; no Cloud auth claim.
