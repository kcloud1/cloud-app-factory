# Intent: reusable Cloud App Factory

Status: ACCEPTED
Owner: Amit
Owning issue: https://github.com/kcloud1/cloud-app-factory/issues/1
Acceptance evidence: Issue #1 records Amit's Option 4 approval on 2026-10-10;
current conversation explicitly says “GO — CLOUD APP FACTORY | M0–M1”, record
accepted intent and implement autonomously. Later instruction permits Codex
review/merge of M0–M1; M2 stays gated.

## Originator words and desired outcome

“Build a reusable Cloud App Factory where Amit provides four answers, Codex Cloud
develops an application, and an approved GitHub/Cloudflare pipeline deploys each
application independently.” Avoid repeat setup after one-time app authorization.

## Problem and users

Amit needs repeatable personal app intake/development/release with isolated
identities and bounded cost. Amit originates/operates; Codex develops; G can review.
M0–M1 produces reviewable dry-run plans, not live apps.

## Current state and discovery

Verified: public repository, default main, clean starting HEAD
`55ed0f8e60bc11242c92a77f2b96aa431650d226`, inherited template contracts/static
example, no open PR or Issue #1 comments at intake. Template guidance read locally;
template main inspected at `6e9ce945106919867c681bcbe2f7bedccbfe5f77`.
Neither reference repository modified.

## Scope and constraints

Initialize README/SPEC/ENV/CONTEXT/INIT and intent. Implement four answers,
deterministic plan, naming/conflicts/authorization gates, reusable Actions dry-run
and future design. Standard library, no new framework, one cohesive PR.
No app repo, Worker, DNS, token, installation, AWS, deploy execution, publication
or spending. Secret values must never be read or exposed.

## Research and open questions

Official [reusable workflow guidance](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows),
[Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)
and [Builds configuration](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/)
inform the separate design. Inherited native-only guidance yields to Issue #1's
Actions design; never use both on one Worker.

Amit reports org secrets configured; repo selection and effective scope remain
unknown. Account identity, domain ownership, live conflicts, Codex Cloud and cost
controls are future gates. Sensitive/private apps need an access/data design.

## Success evidence and authority

Example plan, repeatable digest, malformed-input/collision/authorization checks,
reviewed workflow and one PR/Issue receipt. Local tests are not live proof.
M2's exact owner packet governs first provisioning/exposure. Rollback is a source
revert; no cloud cleanup is needed because M0–M1 creates no cloud resources.
