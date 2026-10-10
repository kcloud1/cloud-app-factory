---
name: aws-cloudops
description: Use for an explicitly AWS-enabled Cloud App Factory project needing optional pinned AWS CLI, SSM/Terraform or Amplify Gen 2 tooling, a credential-free environment check or a future separately authorized AWS task handoff. Do not use for ordinary Cloudflare apps or infer AWS authority from installed software.
---

# AWS Cloud operations toolkit

Read the owning Issue/PR and latest authorized delta first. Use the project's
`AGENTS.md` and accepted intent; load SPEC/ENV only for a concrete authority or
runtime question. Identify exact repository, source SHA and runtime: Codex Cloud,
local CLI and GitHub Actions are separate installation/authentication contexts.
For projects with no AWS needs, make no changes.

Use [the toolkit contract](../../../docs/aws-toolkit.md) for commands, pins,
research sources, adoption example and design-only OIDC conditions. From the
factory root, run `python3 scripts/aws_toolkit.py --plan PROFILE` first. Choose:

- `core`: AWS CLI v2 + gh; credential-free version checks.
- `cloudops`: core + SSM client/Terraform. CLI/CloudWatch/EC2 readback, SSM sessions
  and Terraform plan/readback each need an exact future authorized task. A plan
  can contact providers; it is not a credential-free version check.
- `app-dev`: core + pinned project-local Amplify Gen 2. Provide the exact existing
  `--project-dir`; check only `ampx --version`, never sandbox or deployment.

Install only with explicit project opt-in. Record the reviewed factory full SHA,
profile, absolute prefix/project directory, version receipt and app-dev lock
hash in a short project `env-profile` handoff. Keep PATH changes task-local,
provider locks per-project, and large SDK trees/credentials out of the handoff.
For a copied skill, preserve a link to the same SHA-pinned toolkit contract.

Software setup grants no AWS authority. M6 allows **no** credentials or service
calls. For a future separately authorized operation, first establish caller
identity, exact account and region using the approved authentication context.
A profile name does not prove identity. Personal examples/default future approved
read-only target: account `333438771545`, region `ap-southeast-1`. Official DEV
`672172129528`, PROD and all other accounts are excluded unless explicitly named
and approved. Stop on any identity mismatch, unknown authorization or paid need.

Never infer permission for IAM, provisioning, spend, instance start/stop, SSM
commands/sessions, Terraform apply/destroy/import/state/backend changes or Amplify
sandbox/deploy. The SSM plugin does not provide private connectivity: caller and
destination IAM, agent health and VPC paths require independent approval/proof.
Do not silently add Tailscale, proxies, services or background daemons.

Future GitHub Actions OIDC needs an exact repo/protected branch or environment,
exact audience, short-lived least-privilege role and reviewed trust policy.
Designing this grants no role/provider mutation. Codex Cloud authentication is a
separate trust boundary; never assume a GitHub job token exists there. Do not
copy keys, `.env`, SSO caches or corporate credentials into Cloud/Vault/secrets.
Return compact version/capability evidence and one next action; distinguish
software PASS from unverified authenticated/cloud acceptance.
