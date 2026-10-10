# M0–M1 validation receipt

Owning issue: https://github.com/kcloud1/cloud-app-factory/issues/1
Starting revision: `55ed0f8e60bc11242c92a77f2b96aa431650d226`.
Exact implementation/merge revisions are recorded in the linked PR and Issue receipt.

- Python 3.12.3: `python3 -m unittest discover -s tests -v` — 5 PASS.
- Two CLI invocations matched byte-for-byte and matched `examples/plan.json`.
- Interactive mode accepted exactly four answers and produced that same JSON.
- actionlint 1.7.12 (temporary validation tool, no repository dependency) — PASS.
- `git diff --check` — PASS; actual implementation/governance diff reviewed.

Negative coverage: invalid slug/DNS/budget/schema, unsupported dual pipeline,
malformed inventory, duplicate JSON keys, sanitized parse errors, explicit deploy
rejection, case-insensitive resource collisions, private/sensitive app review,
spending/preview requests, and execution remaining disabled with empty inventory.

M0 complete: accepted intent and initialized contracts. M1 complete: strict
four-answer intake, deterministic offline plans, naming/conflict gates, isolated
Worker convention, mutually exclusive pipeline requirement, reusable dry-run YAML
and exact future owner packet. Five standard-library tests protect stable parsing
and authorization boundaries; no new framework or runtime dependencies.

No GitHub Actions run, Cloudflare call, resource provisioning, secret-value read,
deployment or browser acceptance was performed. Org-secret selection, effective
token permissions/validity, live conflicts/domains and Codex Cloud remain unverified.
No cloud resources need cleanup. Follow-up Issues #2–#4 retain their own gates;
merge authority for M0–M1 came from Amit's explicit updated conversation instruction.
