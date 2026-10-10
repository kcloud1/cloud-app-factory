# Environment

Status: NOT_READY

Record project-specific runtime and dependency truth here. Keep machine-specific facts in the active `~/.agent/HOST.md` profile when available instead of duplicating host configuration in every repository.

## Runtime

- Primary host/profile: `~/.agent/HOST.md` when available
- Working directory: `<repo path>`
- Runtime: `<local | Codex Cloud | container | hosted app | mixed>`

## Development Tools

List only tools this project actually depends on, for example:

- Python: `<version / not required>`
- Node.js / npm: `<version / not required>`
- Docker/Podman: `<required / not required>`
- Terraform/Terragrunt: `<required / not required>`
- Nextflow: `<required / not required>`

## Cloud

- Provider: `<AWS / none / other>`
- AWS profile: `<profile or N/A>`
- Region: `<region or N/A>`
- Account/environment alias: `<personal lab / dev / nonprod / prod / N/A>`

Never infer execution authority from an AWS profile name. Authority comes from `SPEC.md` and the active Issue/instruction.

## External Dependencies

- `<service, MCP, model platform, database, API, or N/A>`

## Optional Cloud-First App

After project intent is accepted, use the [quickstart](docs/CLOUD_FIRST_QUICKSTART.md).
Choosing a provider is opt-in; this template has no cloud runtime or provisioning default.
Record only the fields needed by the selected app:

- App slug / exact repository / Worker or hosting app name: `<values>`
- Provider account alias / environment / visibility / cost limit: `<values>`
- Production branch / deploy root / command: `<main / root / provider command>`
- Approved custom hostname / DNS configuration owner: `<values or N/A>`
- Non-production preview policy / command / URL visibility: `<disabled or approved>`
- GitHub App repository grant / owner onboarding evidence: `<Issue reference>`
- Build credential scope confirmed by owner/provider: `<evidence reference; no value>`

For Cloudflare, follow [owner onboarding](docs/CLOUDFLARE_WORKERS_ONBOARDING.md).
`<app-name>.amitk.life` is this owner's optional production convention, not a universal
zone or account. Domain, Worker creation and credential changes require explicit scope.
Use the [release receipt](docs/DEPLOYMENT_EVIDENCE.md) for runtime proof; keep `ENV.md`
current-only and preserve generic `NOT_READY` until the new project's readiness is known.

## Credentials And Secrets

Use approved local, cloud, or secret-management mechanisms. Never commit credentials, tokens, private keys, or raw secrets.

## Readiness

Set `Status` to `READY` only when the dependencies needed for the current milestone are known and usable. Use `PARTIAL` when missing dependencies do not block the approved work.
