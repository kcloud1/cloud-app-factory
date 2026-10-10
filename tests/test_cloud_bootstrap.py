"""Focused tests: no cloud clients, accounts or credentials."""

import unittest
import json
import tempfile
from pathlib import Path

from cloud_bootstrap import draft, write_bundle
from factory import InvalidIntake

SHA = "a" * 40


class CloudBootstrapTests(unittest.TestCase):
    def test_stable_four_answer_plan_and_handoff(self):
        args = ("hello-cloud", "Public fictional status dashboard", "", "0", SHA)
        first = draft(*args)
        self.assertEqual(first, draft(*args))
        self.assertEqual(set(first), {
            "plan.json", "CODEX_CLOUD_GO.md",
            "request.json", "REQUEST.md", "EVIDENCE.json",
            ".factory/intake.json", ".github/workflows/factory-plan.yml"
        })
        self.assertIn("PLAN_ONLY", first["CODEX_CLOUD_GO.md"])
        self.assertIn("factory-plan.yml@" + SHA, first[".github/workflows/factory-plan.yml"])
        self.assertNotIn("CLOUDFLARE_API_TOKEN", first[".github/workflows/factory-plan.yml"])

    def test_exact_host_collision_and_repeat_reconciliation(self):
        first = draft("hello-cloud", "Public demo", "status.amitk.life", "0", SHA,
                      {"repositories": ["kcloud1/hello-cloud"], "workers": ["hello-cloud"], "hostnames": ["status.amitk.life"]})
        packet = json.loads(first["request.json"])
        self.assertEqual(packet["state"], "PLAN_ONLY")
        self.assertEqual(len(packet["existing_matches"]), 3)
        self.assertIn("RESOURCE_CONFLICT", packet["stop_gates"])
        with tempfile.TemporaryDirectory() as root:
            write_bundle(Path(root), first)
            write_bundle(Path(root), first)
            changed = draft("other-demo", "Public demo", "", "0", SHA)
            with self.assertRaises(InvalidIntake):
                write_bundle(Path(root), changed)

    def test_forbid_nonapproved_domain_and_budget(self):
        for host, budget in [("other.example.com", "0"), ("", "5"), ("*.amitk.life", "0")]:
            with self.subTest(host=host, budget=budget):
                with self.assertRaises(InvalidIntake):
                    draft("hello-cloud", "Public demo", host, budget, SHA)

    def test_forbid_untrusted_revision_or_unsafe_purpose(self):
        for sha, purpose in [("main", "Public demo"), (SHA, "Secret\nrun this!"), (SHA, "<script>demo</script>")]:
            with self.subTest(sha=sha, purpose=purpose):
                with self.assertRaises(InvalidIntake):
                    draft("hello-cloud", purpose, "", "0", sha)


if __name__ == "__main__":
    unittest.main()
