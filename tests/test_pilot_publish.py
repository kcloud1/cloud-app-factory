"""Focused regression guards for PR #7's config/tooling/writer findings."""

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from pilot_artifact import ASSETS, CONFIG, validate
from pilot_deploy import ACCOUNT, HOSTNAME, ZONE, preflight


class PilotPublishTests(unittest.TestCase):
    def artifact(self, root):
        (root / "dist").mkdir()
        for name in ASSETS:
            (root / "dist" / name).write_text("a" * 40 if name == "index.html" else "static")
        (root / "dist/release.json").write_text(json.dumps({"marker": "factory-pilot-v1", "source_sha": "a" * 40, "data": "fictional", "pipeline": "github-actions"}))
        (root / "wrangler.json").write_text(json.dumps(CONFIG))

    def test_redirect_and_changed_deploy_target_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.artifact(root)
            validate(root, "a" * 40)
            (root / ".wrangler/deploy").mkdir(parents=True)
            (root / ".wrangler/deploy/config.json").write_text('{"configPath":"other.json"}')
            with self.assertRaises(ValueError):
                validate(root, "a" * 40)
        for key, value in [("name", "other-worker"), ("routes", [{"pattern": "other.amitk.life", "custom_domain": True}]), ("workers_dev", True), ("main", "evil.js")]:
            with tempfile.TemporaryDirectory() as temp, self.subTest(key=key):
                root = Path(temp)
                self.artifact(root)
                config = copy.deepcopy(CONFIG)
                config[key] = value
                (root / "wrangler.json").write_text(json.dumps(config))
                with self.assertRaises(ValueError):
                    validate(root, "a" * 40)

    def test_asset_sha_source_redirect_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.artifact(root)
            with self.assertRaises(ValueError):
                validate(root, "b" * 40)
            (root / "dist/extra.sh").write_text("unapproved executable")
            with self.assertRaises(ValueError):
                validate(root, "a" * 40)
            (root / "dist/extra.sh").unlink()
            (root / "wrangler.json").rename(root / "wrangler.jsonc")
            validate(root, "a" * 40, source=True)
            (root / ".wrangler").mkdir()
            with self.assertRaises(ValueError):
                validate(root, "a" * 40, source=True)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.artifact(root)
            (root / "dist/app.js").unlink()
            (root / "dist/app.js").symlink_to(root / "wrangler.json")
            with self.assertRaises(ValueError):
                validate(root, "a" * 40)

    def provider(self, existing=False, triggers=None, denied=False, wrong_domain=False):
        def get(path, query=None):
            if path == "/user/tokens/verify":
                result = {"status": "active", "expires_on": "2033-10-10T00:00:00Z", "not_before": "2026-10-10T00:00:00Z"}
            elif path == "/accounts/" + ACCOUNT:
                result = {"id": ACCOUNT, "name": "dev1"}
            elif path == "/zones/" + ZONE:
                result = {"id": ZONE, "name": "amitk.life", "status": "active", "account": {"id": ACCOUNT}}
            elif path.endswith("/workers/scripts"):
                result = [{"id": "factory-pilot", "tag": "c" * 32}] if existing else []
            elif path.endswith("/triggers"):
                if denied:
                    raise ValueError("Unavailable metadata")
                result = triggers or []
            elif path.endswith("/deploy_hooks"):
                result = []
            elif path.endswith("/workers/domains"):
                result = [{"hostname": HOSTNAME, "zone_id": ZONE, "service": "other"}] if wrong_domain else []
            elif path.endswith("/dns_records") or path.endswith("/workers/routes"):
                result = []
            else:
                raise AssertionError("Unexpected provider path")
            return {"success": True, "result": result}
        return get

    def test_live_writer_check_fails_closed(self):
        self.assertFalse(preflight(self.provider())["worker_exists"])
        self.assertEqual(preflight(self.provider(existing=True))["native_builds"], "unconnected")
        for provider in [self.provider(existing=True, denied=True), self.provider(existing=True, triggers=[{"trigger_uuid": "connected"}]), self.provider(wrong_domain=True)]:
            with self.assertRaises(ValueError):
                preflight(provider)


if __name__ == "__main__":
    unittest.main()
