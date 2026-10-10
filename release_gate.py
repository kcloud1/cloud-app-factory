"""No-write release contract checker. Never promotes a plan to live authority."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from factory import InvalidIntake, canonical, fields, hostname, plan, read_json, slug


def full_sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def check(document, registry, context):
    # Recompute both the digest and the planner output, preventing altered target
    # fields from being accepted even if a caller recomputes a forged digest.
    if not isinstance(document, dict) or not isinstance(document.get("plan_id"), str):
        raise InvalidIntake("Plan required")
    unsigned = {k: v for k, v in document.items() if k != "plan_id"}
    if hashlib.sha256(canonical(unsigned).encode()).hexdigest() != document["plan_id"]:
        raise InvalidIntake("Plan digest mismatch")
    expected = plan(document.get("intake"), context.get("inventory"))
    if canonical(expected) != canonical(document):
        raise InvalidIntake("Plan must match the current planner and inventory")
    fields(registry, ["schema_version", "applications"])
    if type(registry["schema_version"]) is not int or registry["schema_version"] != 1 or not isinstance(registry["applications"], list):
        raise InvalidIntake("Invalid allowlist")
    target = document["target"]
    blockers = ["M2_PUBLISH_DISABLED", "LIVE_PROVIDER_READBACK_REQUIRED",
                "CREDENTIAL_SCOPE_AND_EXPIRATION_READBACK_REQUIRED", "SECRET_REPO_SELECTION_READBACK_REQUIRED",
                "PIPELINE_EXCLUSIVITY_READBACK_REQUIRED", "DOMAIN_AND_BUDGET_READBACK_REQUIRED"]
    if not full_sha(context.get("factory_revision")) or context.get("factory_revision") != context.get("checked_out_factory_revision"):
        blockers.append("FACTORY_REVISION_MISMATCH")
    if not full_sha(context.get("source_sha")):
        blockers.append("INVALID_SOURCE_SHA")
    if context.get("repository") != target["repository"]:
        blockers.append("CALLER_REPOSITORY_MISMATCH")
    if context.get("worker") != target["worker"]:
        blockers.append("CALLER_WORKER_MISMATCH")
    if context.get("event") not in ["push", "workflow_dispatch"] or context.get("ref") != "refs/heads/main" or context.get("ref_protected") is not True:
        blockers.append("UNTRUSTED_EVENT_OR_REF")
    if document["architecture"]["pipeline"] != "github-actions":
        blockers.append("WRONG_PIPELINE")
    if document["conflicts"]:
        blockers.append("RESOURCE_CONFLICT")
    if target["repository_visibility"] != "public" or target["application_visibility"] != "public" or document["intake"]["purpose_and_data"]["sensitivity"] != "public":
        blockers.append("UNSUPPORTED_PRIVATE_OR_SENSITIVE_APP")
    if document["intake"]["deployment_and_budget"]["previews"] != "disabled" or document["intake"]["deployment_and_budget"]["paid_services"] != "forbidden":
        blockers.append("ADDITIONAL_EXPOSURE_OR_SPENDING_REVIEW")
    # Presence is supplied as boolean metadata only. No secret values are read.
    if context.get("token_present") is not True or context.get("account_id_present") is not True:
        blockers.append("CREDENTIAL_AVAILABILITY_UNVERIFIED")
    applications = registry["applications"]
    entry_fields = ["repository", "worker", "hostname", "account_alias", "plan_id", "source_sha",
                    "approval_reference", "credential_scope_reference", "secret_selection_reference", "token_expiration_reference",
                    "native_builds_disabled_reference", "budget_reference", "domain_ownership_reference"]
    for entry in applications:
        fields(entry, entry_fields)
        if any(not isinstance(value, str) or not value for value in entry.values()):
            raise InvalidIntake("Incomplete registry evidence")
        if not full_sha(entry["source_sha"]) or not re.fullmatch(r"[0-9a-f]{64}", entry["plan_id"]):
            raise InvalidIntake("Registry revisions must be immutable")
        slug(entry["worker"])
        hostname(entry["hostname"])
        if not entry["repository"].startswith("kcloud1/") or entry["account_alias"] != "dev1":
            raise InvalidIntake("Registry outside approved organization/account")
        slug(entry["repository"].removeprefix("kcloud1/"))
    # Registry comes from the reviewed factory checkout, never a caller-provided
    # file. A matching row is evidence to review, not independently verified truth.
    matches = [x for x in applications if x["repository"] == target["repository"]]
    if len(matches) != 1:
        blockers.append("EXACT_OWNER_APPROVAL_REQUIRED" if not matches else "AMBIGUOUS_OWNER_APPROVAL")
    else:
        approved = matches[0]
        for key in ["repository", "worker", "hostname", "account_alias"]:
            if approved[key] != target[key]:
                blockers.append("APPROVED_TARGET_MISMATCH")
        if approved["plan_id"] != document["plan_id"]:
            blockers.append("APPROVED_PLAN_MISMATCH")
        if approved["source_sha"] != context.get("source_sha"):
            blockers.append("APPROVED_SOURCE_SHA_MISMATCH")
        # One worker/hostname cannot be assigned to two different applications.
        if any(x is not approved and (x["worker"] == approved["worker"] or x["hostname"] == approved["hostname"]) for x in applications):
            blockers.append("DUPLICATE_DEPLOYMENT_WRITER")
    return {"schema_version": 1, "state": "APPROVAL_REQUIRED", "operations_state": "PLAN_ONLY",
            "execution_allowed": False, "publish_enabled": False, "plan_id": document["plan_id"],
            "source_sha": context.get("source_sha") if full_sha(context.get("source_sha")) else None,
            "factory_revision": context.get("factory_revision") if full_sha(context.get("factory_revision")) else None,
            "target": target, "blockers": sorted(set(blockers)),
            "owner_packet": {"repository": target["repository"], "visibility": target["repository_visibility"],
                             "account_alias": target["account_alias"], "worker": target["worker"], "hostname": target["hostname"],
                             "pipeline": document["architecture"]["pipeline"], "monthly_budget_usd": document["intake"]["deployment_and_budget"]["monthly_budget_usd"],
                             "workers_dev": False, "preview_urls": False,
                             "secret_context": "exact selected app caller repository; explicit mapping",
                             "github_app": "no Cloudflare Builds installation needed for Actions",
                             "codex_cloud": "owner-selected environment; unverified",
                             "rollback": "approved known-good version or source revert; no action authorized here"}}


def inside(root, value):
    candidate = (root / value).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file():
        raise InvalidIntake("File must stay in caller checkout")
    return candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--caller-root", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--inventory")
    parser.add_argument("--context", required=True, help="Non-secret runtime metadata JSON")
    parser.add_argument("--mode", choices=["dry-run"], default="dry-run")
    args = parser.parse_args()
    try:
        root = Path(args.caller_root).resolve()
        context = read_json(args.context)
        if not isinstance(context, dict):
            raise InvalidIntake("Metadata must be an object")
        if "inventory" in context:
            raise InvalidIntake("Use an explicit inventory file")
        context["inventory"] = read_json(inside(root, args.inventory)) if args.inventory else None
        report = check(read_json(inside(root, args.plan)), read_json(Path(__file__).with_name("release-targets.json")), context)
    except (ValueError, OSError):
        print("Invalid release input. No action taken.", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
