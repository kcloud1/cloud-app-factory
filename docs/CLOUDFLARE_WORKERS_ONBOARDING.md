# Cloudflare Workers owner onboarding (opt-in)

Use this provider-specific path only after the project's accepted intent chooses
Cloudflare. The universal template and its `INIT.md` contract stay provider-neutral.
Start with the [cloud-first quickstart](CLOUD_FIRST_QUICKSTART.md) and the optional
[static example](../examples/cloudflare-static/README.md). This guide creates nothing.

## Naming and environments

| Item | Convention | Example |
| --- | --- | --- |
| App slug / new repository / new Worker | Lowercase kebab-case; choose once | `status-board` |
| Production branch | `main` | `main` |
| Owner's production hostname | `<app-name>.amitk.life` | `status-board.amitk.life` |
| Other owners | Use a domain they control | `status-board.example.com` |
| Review environment | Explicitly enabled non-production version URL | `workers.dev` version URL |

Record the repository, account alias, exact Worker name, root directory, branch,
hostname, visibility, preview policy and cost boundary in the new project's `ENV.md`.
Existing names are preserved: the reference uses Worker `cloud-ops-demo` with hostname
`cloud-ops.amitk.life`. Do not rename or duplicate an existing Worker to enforce a convention.
`PERSONAL` / `WORK` and `DEV` / `PROD` remain authority classifications from `SPEC.md`;
a production branch alone grants no production permissions.

## One first-time owner authorization gate

Prepare the app/config and a reviewable PR first. Present one concrete onboarding
packet to the owner: exact repository/account/Worker/hostname, public exposure, main
branch, preview choice, required credential scope and resource/cost limits. The owner
approves the GitHub App grant and provider setup together. Approval is project-specific;
record its evidence in the owning Issue. Routine releases inside that approved boundary
do not require repeated GO. A missing permission or scope change remains a real blocker.

Use this new-project checklist in order:

- [ ] Create the app repo from the template only when authorized; reuse it and its Codex
  Cloud session when already present. Complete `INIT.md` with accepted project intent.
- [ ] Adopt the optional six-file starter, personalize it, and prepare one cohesive PR.
  Keep account identifiers/credentials out of the example. Review the asset allowlist.
- [ ] Owner grants Cloudflare's GitHub App access to the **exact repository** (for an
  organization, confirm its owner-approved installation). Codex's GitHub connection
  and ChatGPT's Cloudflare connection do not grant Builds repository access.
- [ ] In Workers & Pages, select the exact existing Worker. For a new app, Worker creation
  is a separately explicit item in the same owner packet; stop if it was not authorized.
  Match `wrangler.jsonc` name to that Worker. Never create a replacement to bypass a blocker.
- [ ] Owner verifies an existing build credential's deployment permissions for this account
  and Worker, plus any approved domain operation. Check permission/resource scope and
  validity through an authorized provider UI/API; token name or a prior successful deploy
  is not scope verification. Never reuse another project's token on that basis. If scope
  cannot be read/confirmed or no suitable credential exists, stop with the exact owner
  action; creation or widening needs explicit credential authority. Keep token **values**
  only in provider-managed credential storage, never code, docs, Issues, PRs or logs.
- [ ] Attach only the exact production Custom Domain in the owner's active Cloudflare zone:
  Settings → Domains & Routes → Add → Custom Domain. Confirm hostname ownership and any
  existing record conflict before changing it. Let the provider manage its exact DNS record
  and certificate. No wildcard DNS, broad zone edits, nameserver changes or preview domains.
  The route-free starter explicitly sets `workers_dev: false` as well as
  `preview_urls: false`; disabling version URLs alone does **not** disable the
  production `workers.dev` hostname. Verify the approved Custom Domain responds
  and the unapproved `workers.dev` production endpoint is disabled. If the owner
  deliberately chooses `workers.dev` instead, approve and record that public
  hostname in `ENV.md` and explicitly set `workers_dev: true` in the adopted app.
- [ ] Connect the existing Worker's Settings → Builds to the exact GitHub repository.
  Set production `main`, root `/` for the copied starter, **empty build command**,
  deploy **`npx wrangler deploy`**, auto-build enabled, and the verified build credential.
  Do not add GitHub Actions or a manual upload as a substitute. A missing build config
  (`12040` in the reference) needs this connection; a manual deploy cannot prove it.
- [ ] Decide previews in the same owner packet. The starter disables `preview_urls`;
  leave preview/non-production builds off unless explicitly approved. For this static,
  credential-free path, enable `preview_urls: true` and use **`npx wrangler versions upload`**
  as the non-production command to produce version URLs without promoting production.
  Current Builds also offers `npx wrangler preview` for named Previews; that separate
  resource/isolation model is outside this minimal path. Never use `wrangler deploy` on
  feature branches against the production Worker. No custom-domain previews (they can
  create wildcard records). Version URLs are public unless protected; accept that boundary.
- [ ] Confirm the native connection and branch policy **before** merging the release PR.
  Squash-merge only when repository authority allows it. Collect exact push/build/deployment
  evidence and exactly two live interactions using the [receipt](DEPLOYMENT_EVIDENCE.md).

## Keep domain ownership explicit

Use one configuration owner. If the domain is dashboard-managed, leave `routes` out
of the starter and read back its binding and HTTPS after every release. If the accepted
project deliberately adopts Wrangler-managed domains, add only the already-approved
exact hostname to that app's config:

```jsonc
"routes": [{ "pattern": "status-board.amitk.life", "custom_domain": true }]
```

This is a property fragment, not a runnable provisioning instruction. Declaring it
can create/change DNS and certificates on deploy; do so only within the owner packet's
authority and confirmed token scope. Never replace a domain's existing record blindly.

## Evidence and recovery

A merge, a successful clone or a manual deployment alone is not an automatic release.
Use [DEPLOYMENT_EVIDENCE.md](DEPLOYMENT_EVIDENCE.md) for the receipt and recovery path.
The [Level 4 proof](https://github.com/kcloud1/cloud-ops-demo/issues/5#issuecomment-6094650672)
shows the proven minimal source/ASSETS pattern. Its token-scope follow-up is a lesson,
not permission to reuse that credential for another app.

Current provider references: [Build configuration](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/),
[branch policy](https://developers.cloudflare.com/workers/ci-cd/builds/build-branches/),
[Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/),
[version URLs](https://developers.cloudflare.com/workers/versions-and-deployments/version-urls/).
