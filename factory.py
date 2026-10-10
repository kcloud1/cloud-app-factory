"""Offline four-answer planner. No provider clients or deployment path."""

import argparse
import hashlib
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


class InvalidIntake(ValueError):
    pass


def fields(value, expected):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise InvalidIntake("Expected fields: " + ", ".join(expected))
    return value


def choice(value, options):
    if not isinstance(value, str) or value not in options:
        raise InvalidIntake("Expected one of: " + ", ".join(options))
    return value


def slug(value):
    # Conservative common subset for repository, Worker and DNS label names.
    if not isinstance(value, str) or not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", value) or len(value) > 63:
        raise InvalidIntake("Name must be lowercase kebab-case, start with a letter, and be 1–63 characters")
    return value


def hostname(value):
    if not isinstance(value, str) or len(value) > 253 or "." not in value:
        raise InvalidIntake("An exact lowercase DNS hostname is required")
    for label in value.split("."):
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label):
            raise InvalidIntake("Invalid hostname; URLs, wildcards and trailing dots are forbidden")
    if value.split(".")[-1].isdigit():
        raise InvalidIntake("IP addresses are not custom hostnames")
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def plan(intake, inventory=None):
    fields(intake, ["application", "purpose_and_data", "visibility_and_domain", "deployment_and_budget"])
    name = slug(intake["application"])
    purpose = fields(intake["purpose_and_data"], ["purpose", "sensitivity"])
    if not isinstance(purpose["purpose"], str) or not purpose["purpose"].strip() or len(purpose["purpose"]) > 1000:
        raise InvalidIntake("Purpose must be a nonempty description of at most 1000 characters")
    sensitivity = choice(purpose["sensitivity"], ["public", "internal", "sensitive"])
    exposure = fields(intake["visibility_and_domain"], ["repository_visibility", "application_visibility", "hostname"])
    repo_visibility = choice(exposure["repository_visibility"], ["public", "private"])
    app_visibility = choice(exposure["application_visibility"], ["public", "private"])
    host = hostname(exposure["hostname"])
    constraints = fields(intake["deployment_and_budget"], ["pipeline", "monthly_budget_usd", "paid_services", "previews"])
    pipeline = choice(constraints["pipeline"], ["github-actions", "native-builds"])
    choice(constraints["paid_services"], ["forbidden", "requested"])
    choice(constraints["previews"], ["disabled", "requested"])
    budget = constraints["monthly_budget_usd"]
    if not isinstance(budget, str) or not re.fullmatch(r"(?:0|[1-9][0-9]{0,6})(?:\.[0-9]{1,2})?", budget):
        raise InvalidIntake("Budget must be a nonnegative USD decimal string with at most two decimal places")
    try:
        normalized_budget = format(Decimal(budget).quantize(Decimal("0.01")), "f")
    except InvalidOperation as exc:
        raise InvalidIntake("Invalid budget") from exc
    target = {"repository": "kcloud1/" + name, "repository_visibility": repo_visibility,
              "account_alias": "dev1", "worker": name, "hostname": host,
              "application_visibility": app_visibility, "production_branch": "main"}
    blockers = ["M0_M1_NO_EXECUTION_AUTHORITY", "EXACT_TARGET_OWNER_APPROVAL_REQUIRED",
                "CREDENTIAL_AVAILABILITY_AND_SCOPE_UNVERIFIED", "DOMAIN_OWNERSHIP_UNVERIFIED",
                "PIPELINE_EXCLUSIVITY_UNVERIFIED", "BUDGET_ENFORCEMENT_UNVERIFIED",
                "CODEX_CLOUD_ENVIRONMENT_USER_SELECTED"]
    conflicts = []
    if inventory is None:
        blockers.append("RESOURCE_INVENTORY_UNVERIFIED")
    else:
        fields(inventory, ["repositories", "workers", "hostnames"])
        for kind, value in [("repositories", target["repository"]), ("workers", name), ("hostnames", host)]:
            entries = inventory[kind]
            if not isinstance(entries, list) or any(not isinstance(x, str) for x in entries):
                raise InvalidIntake("Inventory entries must be lists of names")
            if value.casefold() in [x.casefold() for x in entries]:
                conflicts.append({"resource": kind, "name": value})
        blockers.append("INVENTORY_FRESHNESS_AND_OWNERSHIP_UNVERIFIED")
        if conflicts:
            blockers.append("RESOURCE_CONFLICT")
    if repo_visibility == "private":
        blockers.append("PRIVATE_REPO_ORG_SECRETS_PLAN_LIMIT")
    if app_visibility == "private" or sensitivity != "public":
        blockers.append("ACCESS_AND_DATA_ARCHITECTURE_REVIEW_REQUIRED")
    if sensitivity != "public" and repo_visibility == "public":
        blockers.append("PUBLIC_REPOSITORY_DATA_REVIEW_REQUIRED")
    if constraints["paid_services"] == "requested":
        blockers.append("SPENDING_APPROVAL_REQUIRED")
    if constraints["previews"] == "requested":
        blockers.append("PUBLIC_PREVIEW_APPROVAL_REQUIRED")
    normalized = {"application": name, "purpose_and_data": purpose,
                  "visibility_and_domain": exposure,
                  "deployment_and_budget": dict(constraints, monthly_budget_usd=normalized_budget)}
    result = {"schema_version": 1, "mode": "dry-run", "execution_allowed": False,
              "intake": normalized, "target": target,
              "architecture": {"pipeline": pipeline, "isolated_worker_per_application": True,
                               "other_pipeline_must_be_disabled": True, "workers_dev": False,
                               "preview_urls": False, "dns_owner": "owner-approved exact custom domain"},
              "conflicts": conflicts, "blockers": sorted(blockers),
              "credential_contract": {"token_secret": "CLOUDFLARE_API_TOKEN",
                                      "account_id_existing_secret": "CLOUDFLARE_ACCOUNT_ID",
                                      "account_id_future_variable": "CLOUDFLARE_ACCOUNT_ID",
                                      "inherit_secrets": False},
              "acceptance": ["approved exact repository/account/Worker/hostname and budget",
                             "fresh resource and pipeline readback before execution",
                             "merged SHA equals pipeline source SHA",
                             "active deployment/version targets isolated Worker",
                             "custom-domain HTTPS and two app interactions",
                             "unapproved workers.dev and preview endpoints disabled",
                             "retained resources, cost and rollback receipt"]}
    result["plan_id"] = hashlib.sha256(canonical(result).encode()).hexdigest()
    return result


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise InvalidIntake("Duplicate JSON field")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def interview():
    print("Use public descriptions only; never enter secrets or sensitive data.", file=sys.stderr)
    def ask(prompt):
        print(prompt, file=sys.stderr, end="", flush=True)
        return input()
    return {"application": ask("1. Application name (lowercase slug): "),
            "purpose_and_data": json.loads(ask('2. Purpose and sensitivity (JSON: {"purpose":"…","sensitivity":"public|internal|sensitive"}): ')),
            "visibility_and_domain": json.loads(ask('3. Visibility and domain (JSON: {"repository_visibility":"public|private","application_visibility":"public|private","hostname":"app.amitk.life"}): ')),
            "deployment_and_budget": json.loads(ask('4. Deployment and budget (JSON: {"pipeline":"github-actions|native-builds","monthly_budget_usd":"0","paid_services":"forbidden|requested","previews":"disabled|requested"}): '))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--intake", help="Four-answer JSON file; otherwise ask four questions")
    parser.add_argument("--inventory", help="Optional offline names snapshot; never grants authority")
    parser.add_argument("--mode", choices=["dry-run"], default="dry-run")
    args = parser.parse_args()
    try:
        result = plan(read_json(args.intake) if args.intake else interview(),
                      read_json(args.inventory) if args.inventory else None)
    except (ValueError, OSError, EOFError):
        # Do not echo potentially sensitive input or JSON parser excerpts.
        print("Invalid intake or inventory. Check the documented schema; no action taken.", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
