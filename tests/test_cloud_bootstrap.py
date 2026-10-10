"""Focused tests: no cloud clients, accounts or credentials."""

import unittest

from cloud_bootstrap import draft
from factory import InvalidIntake

SHA = "a" * 40


class CloudBootstrapTests(unittest.TestCase):
    def test_stable_four_answer_plan_and_handoff(self):
        args = ("hello-cloud", "Public fictional status dashboard", "", "0", SHA)
        first = draft(*args)
        self.assertEqual(first, draft(*args))
        self.assertEqual(set(first), {
            "plan.json", "CODEX_CLOUD_GO.md",
            ".factory/intake.json", ".github/workflows/factory-plan.yml"
        })
        self.assertIn("PLAN_ONLY", first["CODEX_CLOUD_GO.md"])
        self.assertIn("factory-plan.yml@" + SHA, first[".github/workflows/factory-plan.yml"])
        self.assertNotIn("CLOUDFLARE_API_TOKEN", first[".github/workflows/factory-plan.yml"])

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
