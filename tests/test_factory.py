"""Focused regression guards for validation and authorization boundaries."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from factory import InvalidIntake, canonical, plan

ROOT = Path(__file__).resolve().parents[1]


class FactoryBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.intake = json.loads((ROOT / "examples/intake.json").read_text())

    def test_deterministic_and_never_authorized(self):
        first = plan(self.intake)
        self.assertEqual(canonical(first), canonical(plan(dict(reversed(list(self.intake.items()))))))
        self.assertFalse(first["execution_allowed"])
        self.assertIn("RESOURCE_INVENTORY_UNVERIFIED", first["blockers"])
        empty = {"repositories": [], "workers": [], "hostnames": []}
        result = plan(self.intake, empty)
        self.assertFalse(result["execution_allowed"])
        self.assertIn("INVENTORY_FRESHNESS_AND_OWNERSHIP_UNVERIFIED", result["blockers"])
        changed = copy.deepcopy(self.intake)
        changed["deployment_and_budget"]["monthly_budget_usd"] = "1"
        self.assertNotEqual(first["plan_id"], plan(changed)["plan_id"])

    def test_collisions_are_not_reuse_permission(self):
        inventory = {"repositories": ["KCLOUD1/STATUS-BOARD"], "workers": ["status-board"],
                     "hostnames": ["STATUS-BOARD.AMITK.LIFE"]}
        result = plan(self.intake, inventory)
        self.assertEqual(len(result["conflicts"]), 3)
        self.assertIn("RESOURCE_CONFLICT", result["blockers"])
        self.assertFalse(result["execution_allowed"])

    def test_malformed_inputs_fail_closed(self):
        cases = [("application", None, x) for x in ["Bad", "-bad", "bad-", "bad--name", "a" * 64, "../other", 4]]
        cases += [("visibility_and_domain", "hostname", x) for x in
                  ["*.amitk.life", "https://app.amitk.life", "app.amitk.life.", "127.0.0.1", "App.amitk.life", "a..life"]]
        cases += [("deployment_and_budget", "monthly_budget_usd", x) for x in ["NaN", "Infinity", "-1", "0.001", 0, "1e9"]]
        cases += [("deployment_and_budget", "pipeline", ["github-actions", "native-builds"])]
        for section, key, value in cases:
            intake = copy.deepcopy(self.intake)
            if key is None:
                intake[section] = value
            else:
                intake[section][key] = value
            with self.subTest(section=section, value=value), self.assertRaises(InvalidIntake):
                plan(intake)
        with self.assertRaises(InvalidIntake):
            plan(dict(self.intake, authorization=True))
        with self.assertRaises(InvalidIntake):
            plan(self.intake, {"repositories": [], "workers": "wrong", "hostnames": []})

    def test_privacy_cost_and_exclusive_pipeline(self):
        intake = copy.deepcopy(self.intake)
        intake["purpose_and_data"]["sensitivity"] = "sensitive"
        intake["visibility_and_domain"].update(repository_visibility="private", application_visibility="private")
        intake["deployment_and_budget"].update(paid_services="requested", previews="requested", pipeline="native-builds")
        result = plan(intake)
        for gate in ["PRIVATE_REPO_ORG_SECRETS_PLAN_LIMIT", "ACCESS_AND_DATA_ARCHITECTURE_REVIEW_REQUIRED",
                     "SPENDING_APPROVAL_REQUIRED", "PUBLIC_PREVIEW_APPROVAL_REQUIRED"]:
            self.assertIn(gate, result["blockers"])
        self.assertEqual(result["architecture"]["pipeline"], "native-builds")
        self.assertTrue(result["architecture"]["other_pipeline_must_be_disabled"])
        self.assertFalse(result["architecture"]["preview_urls"])
        self.assertFalse(result["architecture"]["workers_dev"])

    def test_cli_deploy_rejected_and_errors_sanitized(self):
        result = subprocess.run([sys.executable, str(ROOT / "factory.py"), "--mode", "deploy"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "bad.json"
            for payload in ['{"application":"synthetic-private-marker",', '{"application":"first","application":"second"}']:
                source.write_text(payload)
                result = subprocess.run([sys.executable, str(ROOT / "factory.py"), "--intake", str(source)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("synthetic-private-marker", result.stderr)


if __name__ == "__main__":
    unittest.main()
