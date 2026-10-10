# Cloud-first app quickstart (optional)

**Use case:** build, review, and deploy a small cloud application from **Codex Cloud + GitHub + a connected hosting provider**, without a local laptop. This is optional guidance, not a new initialization gate or an AWS execution permission.

## Choose the smallest proven path

- **Existing repo?** Reuse it. For a new meaningful project, create a GitHub repository from [repo-starter](https://github.com/amitkarpe/repo-starter) and initialize the accepted intent via `INIT.md`. No project needs to be derived from the separate AWS CodeBuild POC.
- **Codex Cloud:** Connect exactly that repository/environment, give one complete GO brief, inspect the repo's `AGENTS.md`, accepted intent, `SPEC.md` and `ENV.md` as needed. Deliver one cohesive PR and a focused check. Within explicit low-risk demo authority, review/squash-merge without repeated human GO. Do not self-grant production/IAM/data permissions.
- **Publish one way:** Cloudflare Workers Git integration works for static assets plus a Worker handler. AWS Amplify Hosting Git integration works for a basic static site; plain HTML/CSS/JS need no framework or Node build. Prefer one platform, not two competing pipelines.
- **Initial provider access:** A provider GitHub App / OAuth installation, repository grant, billing acknowledgement or AWS credential trust may still need one-time human action. **Codex Cloud does not inherit a ChatGPT plugin's AWS/Cloudflare session**. A separate AWS CodeConnections `AVAILABLE` connection does **not** attach itself to Amplify's GitHub Hosting integration.
- **Proof before claiming done:** Provider deployment `SUCCEED` or traffic readback **and** the actual page/JS load **and** two browser checks. Record exact Git SHA, deploy mode, account/region, URL, source parity, cleanup and cost status in the owning Issue/PR. One-time manual ZIP/S3/API publication is a snapshot, **not Git-push auto deployment**. Stop when the two acceptance checks pass.

### Repeatable flow

```text
owner intent -> GitHub repo -> Codex Cloud branch / one ready PR
  -> one owner Git/hosting integration gate -> confirm native branch connection
  -> authorized merge -> native push build of exact SHA -> active deployment
  -> custom-domain HTTPS + exactly two live interactions -> Issue evidence -> stop
```

No new CI, Terraform, database, CodeBuild, repository, IAM role or test framework merely to serve a static site. Add those only if the user's next accepted goal actually needs them. No secrets, tokens or SSO caches in Git.

### Optional static Cloudflare path

Copy the [six-file starter](../examples/cloudflare-static/README.md) only after intent
acceptance. Follow the [owner onboarding checklist](CLOUDFLARE_WORKERS_ONBOARDING.md)
for naming, `<app-name>.amitk.life` (or another owner's domain), exact GitHub App grant,
Worker/domain identity, native Builds on `main`, previews and confirmed token scope.
Keep the root template provider-neutral. No new Worker, credentials or DNS are created
by adopting these files; a deployment command can provision and needs explicit authority.

Use the [acceptance receipt](DEPLOYMENT_EVIDENCE.md) for the exact merged SHA,
`push_event` build, deployment/version, HTTPS, two interactions and recovery. Connect
Builds **before** merging the marker PR so the merge can supply the automatic trigger.

### Copy-paste GO for a new Codex Cloud session

```text
GO — Cloud-first deployment of <repository-url>

Goal: <one useful website or workflow>.
Use the existing repository if available; otherwise stop at the
single GitHub template/repository creation action you genuinely need.

Read AGENTS.md, the owning Issue/intent, then SPEC.md and ENV.md only
as relevant. Target environment: <PERSONAL / OFFICIAL DEV / other>;
target hosting provider/account/app/domain: <explicit values or N/A>.
Public data only: <yes/no>. Estimated spend / retained resources: <limit>.
Approved actions: <e.g. code + PR + squash-merge + one personal-demo deployment>.
Anything beyond these actions remains gated.

Use plain HTML/CSS/JS unless the app actually needs another stack.
Create one PR and run proportional checks. Confirm ONE native host connection
before squash-merging when authorized (Cloudflare Workers or another provider).
Use the source-committed deploy configuration when supported.
If a provider connection is missing, report the exact one-time owner GUI
authorization and stop there; never fabricate a token or broaden IAM.
Do not assume a GitHub merge caused a deployment.
Verify the exact merged SHA, native push build/deployment, custom-domain HTTPS
and exactly two relevant live browser interactions.
Write one concise GitHub Issue/PR evidence receipt, including deployment
method (Git-integrated vs manual snapshot) and cleanup. Then STOP.
```

### Real reference, including honest gaps

[Level 4 evidence](https://github.com/kcloud1/cloud-ops-demo/issues/5#issuecomment-6094650672)
now proves GitHub `main` → native Cloudflare `push_event` build → exact merged SHA
→ active deployment → two live browser interactions at the workers.dev URL.
The [custom hostname](https://cloud-ops.amitk.life/) has separate domain/HTTPS fetch
evidence; custom-host browser acceptance was not claimed. Initial Cloudflare and
Amplify releases were manual snapshots; Amplify is outside this reusable Cloudflare
path. Successful use of an existing token did not establish its full permission scope
for future reuse. The [receipt](DEPLOYMENT_EVIDENCE.md#proven-reference-and-its-limits)
preserves the IDs and limits without rerunning prior tests or provisioning another app.
