# Environment

Status: READY (M0–M2 offline implementation only; live prerequisites unresolved)

## Repository/runtime

- Repository: `kcloud1/cloud-app-factory`; PUBLIC; default `main`.
- Checkout: `/home/user/git/cloud-app-factory`.
- Template: `amitkarpe/repo-starter`; inherited governance retained.
- Python 3.10+ standard library; verified locally on Python 3.12.3.
- Git/gh for review and evidence; no Node, Docker, Terraform or AWS requirement.
- Codex Cloud is owner-selected, not provisioned or proven here.

## Future provider contract (unverified)

- Cloudflare alias `dev1` from Issue #1; no account ID inferred.
- Proposed app repo/Worker: `kcloud1/<slug>` / `<slug>`.
- Exact requested hostname; `<slug>.amitk.life` is an owner convention.
- Production branch `main`; root/build command depends on approved app.
- Workers.dev/previews disabled; exactly one Actions or native Builds pipeline.
- Native Builds requires exact GitHub App grant; Actions uses checkout access
  and separately approved deploy credentials.
- AWS profile/account/region: N/A.

## Credentials/readiness

Amit reports org secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`
configured. Factory repo selection, availability, validity and effective scope
remain UNVERIFIED. No values were read or tested. Account ID should be a future
repository/environment variable; existing org secret remains unchanged until
authorized. Do not copy it.

Issue #1 records private-repo org-secret plan limitations; private apps need a
reviewed supported credential/runner path. Availability never proves permission.
M2 must restrict selected repos and confirm account/Worker/domain scope without
values. Future missing dependencies do not block offline M1.

M2 read-only metadata attempt: GitHub org-secret listing returned HTTP 403 because
the current identity lacks required org-secret metadata access. No access refresh
or permission expansion attempted. No authorized Cloudflare UI/API capability is
available in this lane; token scope/expiration/account identity remain UNVERIFIED.
The future reusable release gate accepts only boolean secret-presence signals,
never values, and is not run in this milestone.
