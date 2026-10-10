# Pipeline design and M2 packet

## Implemented now

`factory-plan.yml` creates a dry-run artifact only. Caller intake contains public
descriptions. Pin the workflow and `factory_revision` to the same reviewed SHA:

```yaml
name: Plan application
on: workflow_dispatch
permissions:
  contents: read
jobs:
  plan:
    uses: kcloud1/cloud-app-factory/.github/workflows/factory-plan.yml@<FULL_FACTORY_SHA>
    with:
      intake_path: intake.json
      factory_revision: <FULL_FACTORY_SHA>
```

This caller design is not installed/executed. No secrets block, Wrangler, deploy
action or write permission exists in M1. Separate caller/factory checkouts prevent
caller code replacing planner code. Intake resolves inside caller checkout.
Caller must match the workflow and factory pins; M2 now enforces this using the
job's workflow identity. Artifacts live seven days;
never place private descriptions in this public evidence path. Hosted execution
and artifact upload are unproven until an authorized run.

## Future approved release

The M2 [implemented release gate](RELEASE_GATE.md) checks the future invocation
contract but keeps actual publish disabled. This section describes the later
release path, not runnable deployment in M2.

Amit supplies intake; owner-selected Codex Cloud uses the accepted plan and app
governance to implement in the exact authorized app repository and submits a PR.
Codex Cloud automation is unproven until separately validated.

After review/merge, each approved app's main push calls one reusable deploy workflow.
It checks the immutable app authorization, repo/account/Worker/hostname, plan
digest, source SHA, budget, credential scope and fresh conflicts/ownership. Before
Actions deployment, prove native Builds disabled; inability to read back blocks.
Native Builds apps must have no active Actions deploy caller for that Worker.
Pipeline migration requires approved transition/readback; never overlap.

Each app owns a distinct Worker/exact hostname. Serialize release concurrency
by account + Worker. Plans do not reserve names. Collisions need explicit reuse
authority, not overwrite/automatic rename. Workers.dev/previews default disabled.
Custom-domain configuration can mutate DNS/certificates; no wildcard routes.

Use read-only checkout and explicitly map `CLOUDFLARE_API_TOKEN`, never
`secrets: inherit`. Account ID should be an approved variable named
`CLOUDFLARE_ACCOUNT_ID`; retaining the existing secret requires an explicit
compatibility mapping. Storage remains unchanged in M1. Confirm minimum account/
Workers/domain permissions through owner/provider evidence. Secret repo selection,
presence, token validity and permission scope are separate gates. Metadata checks
record names/selection/presence only. Native Builds also requires exact GitHub App
grant and build credential; Actions requires no Cloudflare App installation.

Future release workflows pin reviewed actions/tool versions, never deploy
untrusted PR code and expose credentials only in approved app release jobs.
Use protected environments with owner-approved release policy. Routine releases
inside standing app approval need no repeated GO; scope/exposure/spend changes do.
Resolve private runner/secret plan limits first. Budget strings do not enforce
hard provider billing caps: usage/quota/alerts and owner acceptance of enforcement
limits are required. No paid service is implicit.

## Exact M2 owner packet (M1 merge grants none of this)

- Exact app repo/visibility, accepted intent, reviewed app SHA and plan digest.
- Verified account privately, isolated Worker and exact hostname.
- Public data or reviewed private access/data design.
- Explicit repo/Worker creation or reuse, DNS/certificate/exposure authority.
- Exactly one pipeline, fresh exclusivity proof and any GitHub App grant.
- Selected-repo credentials, effective scope/validity evidence, account mapping; no values.
- Cost ceiling, usage controls, plan eligibility, paid-service and retention policy.
- Previews/workers.dev decision; root/build command.
- Bounded first release, fresh conflicts, rollback target and cleanup authority.

After approval, prove merged SHA → pipeline/build ID → active deployment/Worker
→ custom-domain HTTPS → two app interactions. Record disabled unapproved endpoints,
retention/cost/scope/rollback in the owning Issue using [the receipt](DEPLOYMENT_EVIDENCE.md).
Reconcile uncertain run IDs before retry. Plans, screenshot, merge and credential
presence do not prove release.

References: [GitHub reusable inputs/secrets](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows),
[Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/),
[Cloudflare Builds](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/).
