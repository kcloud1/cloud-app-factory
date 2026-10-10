---
name: cloud-app-bootstrap
description: Use for a new personal public Cloudflare Workers demo requested from Codex Cloud or mobile. Turn four short answers into the existing Cloud App Factory's deterministic, no-write plan; prepare an exact GitHub repo/Worker/domain handoff; reuse the SHA-pinned shared workflows and enforce the one-writer, owner-approval and secret boundaries. Do not use for AWS, private data, paid infrastructure or unauthorized production changes.
---

# Cloud App Bootstrap

## Input and source

Ask only for app slug, public fictional purpose, exact hostname (default app.amitk.life), and $0 budget. For sensitive/private apps or spending, stop and open a separately approved intake. Use `cloud_bootstrap.py` at repository root and read `AGENTS.md` plus the owning GitHub Issue. Current GitHub/provider truth outranks older handoffs.

## Execute with Codex Cloud

1. From the factory GitHub **Actions** page, run **New cloud app - four answers (plan only)**. This has no provider secrets and creates an artifact with `plan.json`, `CODEX_CLOUD_GO.md`, `.factory/intake.json` and a read-only caller workflow.
2. Read the plan and accept the exact proposed public repo/Worker/hostname before provisioning. A green plan is never a deployment approval.
3. Reuse the repo and published Codex Cloud environment if present. Otherwise surface the one-time GitHub template/repository and Codex Cloud environment authorization. Never claim a local CLI task is Codex Cloud.
4. Use `CODEX_CLOUD_GO.md` inside the actual repo-bound Codex Cloud task. One cohesive PR, review, protected main, exact full SHA, minimal checks.
5. Do not invoke any generic publisher until Issue #3's pilot is live-proven and a shared publishing workflow is independently reviewed/merged. Pin to its full commit SHA and pass only explicitly named caller repo secrets; not `secrets: inherit`.
6. Before first Worker/domain write, verify resource uniqueness, caller secret selection, token scope/expiry, approved exact hostname, $0 policy and native Builds exclusion. Stop on mismatches. Never substitute manual deploy for Git proof.
7. Once authorized, verify Git Actions run, deployed source SHA, Cloudflare version, exact HTTPS domain and two browser interactions; publish evidence.

## Limits

No automatic Cloudflare, GitHub organization or Codex Cloud environment permissions are conferred by this skill. Do not expose secrets, create wildcard DNS, reuse an unrelated Worker, broaden tokens, touch AWS or assume factory secrets automatically flow into called workflows. New repos may require one-time owner authorization under the existing GitHub plan. Keep the M2 no-write gate intact.
