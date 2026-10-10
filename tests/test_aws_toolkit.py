"""Credential-free safety boundaries; no vendor downloads in unit tests."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

spec = importlib.util.spec_from_file_location(
    "aws_toolkit", Path(__file__).resolve().parents[1] / "scripts/aws_toolkit.py")
toolkit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(toolkit)


class ToolkitSafetyTests(unittest.TestCase):
    def test_plan_never_downloads_or_creates_install_prefix(self):
        with tempfile.TemporaryDirectory() as tmp:
            prefix = Path(tmp) / 'not-created'
            with patch.object(toolkit.sys, 'argv', ['aws_toolkit.py', '--plan', 'core',
                                                   '--prefix', str(prefix)]), \
                    patch.object(toolkit, 'download') as download, \
                    patch('builtins.print'):
                self.assertEqual(toolkit.main(), 0)
                download.assert_not_called()
                self.assertFalse(prefix.exists())

    def test_version_subprocess_has_no_caller_credentials_or_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            executable = Path(tmp) / "check"
            executable.write_text(
                "#!/usr/bin/python3\nimport os\n"
                "assert 'AWS_ACCESS_KEY_ID' not in os.environ\n"
                "assert 'GH_TOKEN' not in os.environ\n"
                "assert 'NODE_OPTIONS' not in os.environ\n"
                "assert os.environ['AWS_CONFIG_FILE']=='/dev/null'\n"
                "assert os.environ['HOME']!=os.environ.get('CALLER_HOME')\n"
                "print('1.2.3')\n")
            executable.chmod(0o755)
            with patch.dict('os.environ', {'AWS_ACCESS_KEY_ID': 'test-only',
                                          'GH_TOKEN': 'test-only',
                                          'NODE_OPTIONS': '--invalid'}):
                self.assertEqual(toolkit.run([executable]), '1.2.3')

    def test_checksum_failure_precedes_extraction(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'bin').mkdir()
            class Response:
                def __enter__(self): return self
                def __exit__(self, *args): pass
                def read(self, n):
                    data, self.data = getattr(self, 'data', b'bad archive'), b''
                    return data
            with patch.object(toolkit.urllib.request, 'build_opener') as opener, \
                    patch.object(toolkit, 'extract') as extract:
                opener.return_value.open.return_value = Response()
                with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
                    toolkit.install_binary('aws', root, 'amd64', {'pinned': False})
                extract.assert_not_called()
                self.assertEqual(list((root / 'bin').iterdir()), [])
                self.assertEqual(sorted(p.name for p in root.iterdir()), ['bin'])

    def test_archive_traversal_cannot_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with zipfile.ZipFile(root / 'bad.zip', 'w') as archive:
                archive.writestr('../escaped', 'unsafe')
            with self.assertRaisesRegex(ValueError, 'Unsafe archive path'):
                toolkit.extract(root / 'bad.zip', root / 'extract', 'zip')
            self.assertFalse((root / 'escaped').exists())

    def test_reuse_does_not_download_or_change_prefix(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(toolkit, 'download') as download:
            root = Path(tmp)
            self.assertEqual(toolkit.install_binary('aws', root, 'amd64', {'pinned': True}), 'REUSED')
            self.assertEqual(list(root.iterdir()), [])
            download.assert_not_called()

    def test_existing_project_configuration_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / '.aws-toolkit/app-dev'
            target.mkdir(parents=True)
            package = target / 'package.json'
            package.write_text('existing project tooling')
            with self.assertRaisesRegex(ValueError, 'no project files overwritten'):
                toolkit.install_appdev(root, {'pinned': False})
            self.assertEqual(package.read_text(), 'existing project tooling')

    def test_project_tooling_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / 'project'
            project.mkdir()
            outside = root / 'outside'
            outside.mkdir()
            (project / '.aws-toolkit').symlink_to(outside)
            with self.assertRaisesRegex(ValueError, 'must not be symlinks'):
                toolkit.install_appdev(project, {'pinned': False})
            self.assertEqual(list(outside.iterdir()), [])

    def test_managed_bin_symlink_cannot_redirect_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prefix, outside = root / 'prefix', root / 'outside'
            prefix.mkdir()
            outside.mkdir()
            (prefix / 'bin').symlink_to(outside)
            with patch.object(toolkit, 'download') as download:
                with self.assertRaisesRegex(ValueError, 'real directory'):
                    toolkit.install_binary('aws', prefix, 'amd64', {'pinned': False})
                download.assert_not_called()
            self.assertEqual(list(outside.iterdir()), [])

    def test_dangling_managed_link_does_not_fall_back_to_system_tool(self):
        with tempfile.TemporaryDirectory() as tmp:
            prefix = Path(tmp)
            (prefix / 'bin').mkdir()
            (prefix / 'bin/aws').symlink_to(prefix / 'missing')
            with patch.object(toolkit.shutil, 'which') as which:
                with self.assertRaisesRegex(ValueError, 'Dangling managed aws link'):
                    toolkit.tool_path('aws', prefix, None)
                which.assert_not_called()

    def test_symlinked_lock_does_not_create_external_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prefix = root / 'prefix'
            prefix.mkdir()
            external = root / 'not-created'
            (prefix / '.install.lock').symlink_to(external)
            with self.assertRaises(OSError):
                toolkit.open_install_lock(prefix)
            self.assertFalse(external.exists())

    def test_fifo_lock_is_rejected_without_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            prefix = Path(tmp)
            os.mkfifo(prefix / '.install.lock')
            with self.assertRaisesRegex(ValueError, 'regular, unshared file'):
                toolkit.open_install_lock(prefix)

    def test_hardlinked_lock_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prefix = root / 'prefix'
            prefix.mkdir()
            external = root / 'preserved'
            external.write_text('preserved')
            os.link(external, prefix / '.install.lock')
            with self.assertRaisesRegex(ValueError, 'regular, unshared file'):
                toolkit.open_install_lock(prefix)
            self.assertEqual(external.read_text(), 'preserved')

    def test_same_ampx_version_with_drifted_lock_does_not_pass_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            exe = project / '.aws-toolkit/app-dev/node_modules/.bin/ampx'
            exe.parent.mkdir(parents=True)
            exe.write_text('not executed')
            with patch.object(toolkit, 'version', return_value=toolkit.MANIFEST['tools']['ampx']['version']):
                receipt = toolkit.inventory('app-dev', project / 'prefix', project)
            self.assertFalse(receipt['ampx']['pinned'])

    def test_unsupported_platform_stops_without_install(self):
        with patch.object(toolkit.platform, 'system', return_value='Darwin'):
            with self.assertRaisesRegex(ValueError, 'Supported: Linux'):
                toolkit.architecture()


if __name__ == '__main__':
    unittest.main()
