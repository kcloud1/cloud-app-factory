# Proposed M3 pilot — owner approval required

Owning issue: https://github.com/kcloud1/cloud-app-factory/issues/3
Status: PROPOSED, not approved or reserved. M2 merge grants no resource authority.

| Decision | Proposed exact boundary |
| --- | --- |
| Repository | New public `kcloud1/factory-pilot`, from `amitkarpe/repo-starter` via owner-authorized template flow |
| Application | Fictional public status/demo board, static HTML/CSS/JS; no customer/private data, no AWS/API |
| Development | Owner-selected Codex Cloud environment; existing lane may prepare code after exact app authority |
| Cloudflare | `dev1`; account ID must be verified privately before any write |
| Worker | New isolated `factory-pilot` |
| Domain | Exactly `factory-pilot.amitk.life`, existing `amitk.life` zone; DNS/certificate changes require explicit approval |
| Exposure | Custom hostname public; workers.dev and preview URLs disabled |
| Deploy writer | GitHub Actions app caller only, full reviewed factory pin; native Builds disabled |
| Credentials | Org secrets selected for this exact new caller; minimum operation scope and expiration verified without values |
| Cost | Proposed $0/month, no paid features; owner must accept quota/billing enforcement limits before provision |
| Retention | Retain one pilot Worker/repo/exact domain for evidence until owner-directed cleanup; no automatic deletion |
| Rollback | Stop failed first release and reconcile same run; later known-good version/source revert only under app authority |

App/template creation, Worker creation, exact domain/certificate, org-secret
selection and any token permission change need explicit owner authority. Prefer
owner first provisioning to broadening a recurring deploy token. No Cloudflare
GitHub App installation is needed for Actions. Repository branch protection and
restricted release policy need to be confirmed before release-gate invocation.

Before GO: fresh read-only repo/Worker/hostname/DNS collisions, account/zone
ownership, token scope/expiration, caller secret selection and writer exclusivity.
Org-secret metadata access is currently blocked (403); Cloudflare access unavailable.
Neither an empty snapshot nor this proposed name proves resources free.
Read-only GitHub lookup of `kcloud1/factory-pilot` returned 404 on 2026-10-10;
this means not found/visible to this identity, not reserved or guaranteed available.

After exact approval: one initialized app, one reviewed PR, one Git-triggered
deployment tied to the merged SHA, exact run/deployment/version/domain evidence.
Perform exactly two checks: release marker plus demo button response; theme
toggle with accessible state. Read back HTTPS/assets, disabled unapproved public
endpoints, retained resources and cost. No manual deploy substitutes for proof.

Owner acceptance must be recorded in Issue #3 or its app SPEC; the actual reviewed
app SHA and factory revision will be bound before the bounded first release.
