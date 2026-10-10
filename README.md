# Cloud App Factory

Amit supplies four answers; the factory prepares a repeatable plan for Codex Cloud
to develop an application in its own repository and for an approved pipeline to
release its isolated Cloudflare Worker. M0–M1 delivers **offline planning only**.

## Four answers

1. Application name: a lowercase kebab-case slug.
2. Purpose and data sensitivity: public description plus `public`, `internal` or `sensitive`.
3. Visibility and domain: repository visibility, app visibility and an exact hostname.
4. Deployment and budget: exactly one pipeline, USD ceiling, paid-service and preview policy.

Use Python 3.10+ with no installed dependencies:

```bash
python3 factory.py
python3 factory.py --intake examples/intake.json
python3 -m unittest discover -s tests -v
```

Interactive mode asks exactly four questions; the last three accept JSON objects
shown in their prompts. For repeatable use, edit [the example](examples/intake.json).
Use public descriptions only: plans echo the description and may become public
artifacts. Never enter credentials, customer details or private data.

Output goes to stdout. Malformed input exits 2 with a sanitized error. A valid
blocked plan exits 0 because planning succeeded; consumers must inspect
`execution_allowed` (always false in M1) and `blockers`. Exit 0 never grants approval.
`--mode deploy` is rejected. No network calls or credential reads occur.

Optional `--inventory inventory.json` accepts lists named `repositories`
(full `owner/repo`), `workers` and `hostnames`. Matching is case-insensitive.
Omitting inventory flags unknown conflicts. A snapshot detects collisions but
cannot prove freshness, ownership or absence of live conflicts. Names use a
conservative 1–63 character common subset; hostnames allow exact lowercase DNS
names only. Same input and snapshot produce byte-identical plans and a digest
covering targets, constraints, conflicts and gates. A digest is not authorization.

## Pipeline and next milestone

[Reusable dry-run workflow](.github/workflows/factory-plan.yml) accepts a caller's
intake and reviewed factory SHA, uses read-only permissions and emits a seven-day
artifact without receiving Cloudflare secrets. No workflow automatically triggers
in M1. Public standard GitHub runners are allowed; private runner eligibility needs review.

[Pipeline design and M2 packet](docs/FACTORY_PIPELINE.md) specifies future deployment.
Each app owns a repository, Worker, exact hostname, budget and authorization.
Actions and native Builds must never both deploy the same Worker. Inherited native
onboarding is reference guidance; Issue #1 selects this factory's Actions design.
M2 adds [the no-write release gate](docs/RELEASE_GATE.md), with actual publication
disabled. M3 provisioning remains separately gated after M2 merge.

```bash
python3 release_gate.py --caller-root . --plan examples/plan.json --context examples/release-context.json
```

The synthetic example reports `APPROVAL_REQUIRED` / `PLAN_ONLY`. Exit 0 means
the report was produced, never release readiness. `release-targets.json` is an
empty reviewed factory allowlist; no application has live authority.

Start with [AGENTS.md](AGENTS.md), [accepted intent](intent/0001-project-bootstrap/intent.md),
[SPEC.md](SPEC.md) and [ENV.md](ENV.md) as their read contract requires.
Origin: `kcloud1/cloud-app-factory`, from `amitkarpe/repo-starter`.
No app repository, Worker, DNS, token or deployment is created by this milestone.
The template and `cloud-ops-demo` remain unchanged.
