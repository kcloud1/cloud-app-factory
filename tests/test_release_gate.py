"""Release trust-boundary regression checks; synthetic approvals never grant live authority."""

import copy
import hashlib
import json
import unittest
from pathlib import Path

from factory import InvalidIntake, canonical, plan
from release_gate import check, inside

ROOT = Path(__file__).resolve().parents[1]


class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.document = plan(json.loads((ROOT / "examples/intake.json").read_text()))
        self.registry = {"schema_version": 1, "applications": []}
        self.context = {"repository": "kcloud1/status-board", "worker": "status-board", "source_sha": "a" * 40,
                        "factory_revision": "b" * 40, "checked_out_factory_revision": "b" * 40,
                        "event": "push", "ref": "refs/heads/main", "ref_protected": True,
                        "token_present": False, "account_id_present": False}

    def approval(self):
        entry = {key: self.document["target"][key] for key in ["repository", "worker", "hostname", "account_alias"]}
        entry.update(plan_id=self.document["plan_id"], source_sha=self.context["source_sha"])
        for key in ["approval_reference", "credential_scope_reference", "secret_selection_reference", "token_expiration_reference",
                    "native_builds_disabled_reference", "budget_reference", "domain_ownership_reference"]:
            entry[key] = "synthetic-test-evidence-only"
        return entry

    def test_empty_and_synthetic_approval_never_enable_publish(self):
        report = check(self.document, self.registry, self.context)
        self.assertEqual(report["state"], "APPROVAL_REQUIRED")
        self.assertEqual(report["operations_state"], "PLAN_ONLY")
        self.assertIn("EXACT_OWNER_APPROVAL_REQUIRED", report["blockers"])
        self.assertIn("CREDENTIAL_AVAILABILITY_UNVERIFIED", report["blockers"])
        self.registry["applications"] = [self.approval()]
        self.context.update(token_present=True, account_id_present=True)
        report = check(self.document, self.registry, self.context)
        self.assertFalse(report["execution_allowed"])
        self.assertFalse(report["publish_enabled"])
        self.assertIn("M2_PUBLISH_DISABLED", report["blockers"])
        self.assertIn("LIVE_PROVIDER_READBACK_REQUIRED", report["blockers"])

    def test_tampered_digest_and_rehashed_forgery_rejected(self):
        bad = copy.deepcopy(self.document)
        bad["target"]["worker"] = "unapproved"
        with self.assertRaises(InvalidIntake):
            check(bad, self.registry, self.context)
        unsigned = {k: v for k, v in bad.items() if k != "plan_id"}
        bad["plan_id"] = hashlib.sha256(canonical(unsigned).encode()).hexdigest()
        with self.assertRaises(InvalidIntake):
            check(bad, self.registry, self.context)

    def test_untrusted_ref_repo_sha_pin_and_nonboolean_presence(self):
        cases = [("event", "pull_request", "UNTRUSTED_EVENT_OR_REF"),
                 ("ref", "refs/heads/feature", "UNTRUSTED_EVENT_OR_REF"),
                 ("ref_protected", False, "UNTRUSTED_EVENT_OR_REF"),
                 ("repository", "kcloud1/unapproved", "CALLER_REPOSITORY_MISMATCH"),
                 ("worker", "other", "CALLER_WORKER_MISMATCH"),
                 ("source_sha", "main", "INVALID_SOURCE_SHA"),
                 ("factory_revision", "main", "FACTORY_REVISION_MISMATCH"),
                 ("checked_out_factory_revision", "c" * 40, "FACTORY_REVISION_MISMATCH"),
                 ("token_present", "true", "CREDENTIAL_AVAILABILITY_UNVERIFIED")]
        for key, value, blocker in cases:
            context = dict(self.context, **{key: value})
            with self.subTest(key=key):
                report = check(self.document, self.registry, context)
                self.assertIn(blocker, report["blockers"])
                self.assertFalse(report["execution_allowed"])

    def test_approved_sha_plan_target_and_duplicate_writer(self):
        for key, value, blocker in [("source_sha", "c" * 40, "APPROVED_SOURCE_SHA_MISMATCH"),
                                    ("plan_id", "d" * 64, "APPROVED_PLAN_MISMATCH"),
                                    ("hostname", "other.amitk.life", "APPROVED_TARGET_MISMATCH")]:
            entry = self.approval()
            entry[key] = value
            with self.subTest(key=key):
                report = check(self.document, dict(self.registry, applications=[entry]), self.context)
                self.assertIn(blocker, report["blockers"])
        entry = self.approval()
        other = dict(entry, repository="kcloud1/other")
        report = check(self.document, dict(self.registry, applications=[entry, other]), self.context)
        self.assertIn("DUPLICATE_DEPLOYMENT_WRITER", report["blockers"])
        report = check(self.document, dict(self.registry, applications=[entry, entry]), self.context)
        self.assertIn("AMBIGUOUS_OWNER_APPROVAL", report["blockers"])

    def test_no_private_metadata_or_untrusted_path_output(self):
        context = dict(self.context, arbitrary_secret="synthetic-private-marker")
        self.assertNotIn("synthetic-private-marker", canonical(check(self.document, self.registry, context)))
        with self.assertRaises(InvalidIntake):
            inside(ROOT, "../outside.json")
        self.assertEqual(inside(ROOT, "examples/plan.json"), ROOT / "examples/plan.json")


if __name__ == "__main__":
    unittest.main()
