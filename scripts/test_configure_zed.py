"""Exercise Zed installs with JSONC settings and local keybindings."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


class ConfigureZedTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.config = Path(temporary.name) / "zed"
        self.settings = self.config / "settings.json"
        self.keymap = self.config / "keymap.json"

    def configure(self, stamp, *options, check=True):
        return subprocess.run(
            [
                sys.executable,
                REPO / "scripts/configure-zed.py",
                REPO / "zed",
                self.config,
                stamp,
                *options,
            ],
            capture_output=True,
            text=True,
            check=check,
        )

    def test_merge_preserves_local_values_and_is_idempotent(self):
        self.config.mkdir()
        original = '''{
            // Omazed owns the local theme.
            "theme": "Omazed",
            "ssh_connections": [{"host": "dev.example.test"}],
            "context_servers": {"custom": {"settings": {"key": "local//value,}"}}},
            "lsp": {"jdtls": {"binary": {"path": "/local/jdtls"}}},
        }'''
        self.settings.write_text(original)
        self.keymap.write_text(
            '[{"context":"Workspace","bindings":{"ctrl-k t":null,"f8":"editor::Format",}},]'
        )

        self.configure("first")
        settings = json.loads(self.settings.read_text())
        self.assertTrue(settings["vim_mode"])
        self.assertEqual(settings["theme"], "Omazed")
        self.assertEqual(settings["ssh_connections"], [{"host": "dev.example.test"}])
        self.assertEqual(settings["context_servers"]["custom"]["settings"]["key"], "local//value,}")
        self.assertEqual(settings["lsp"]["jdtls"]["binary"]["path"], "/local/jdtls")

        keymap = json.loads(self.keymap.read_text())
        self.assertEqual(keymap[0]["bindings"], {"f8": "editor::Format"})
        self.assertEqual(keymap[1]["bindings"]["ctrl-k t"], "terminal_panel::Toggle")

        backup = self.config / "settings.json.bak-first"
        self.assertEqual(backup.read_text(), original)
        for path in (backup, self.settings, self.keymap):
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

        self.configure("again")
        self.assertEqual(list(self.config.glob("*.bak-again")), [])

    def test_dry_run_and_legacy_symlink(self):
        self.configure("dry", "--dry-run")
        self.assertFalse(self.config.exists())
        self.config.mkdir()
        target = self.config.parent / "old-settings.json"
        original = '{"vim_mode":false,"theme":"Omazed"}'
        target.write_text(original)
        self.settings.symlink_to(target)

        self.configure("migrate")
        self.assertFalse(self.settings.is_symlink())
        self.assertEqual(target.read_text(), original)
        self.assertEqual((self.config / "settings.json.bak-migrate").read_text(), original)
        self.assertTrue(json.loads(self.settings.read_text())["vim_mode"])

    def test_malformed_keymap_leaves_both_files_alone(self):
        self.config.mkdir()
        self.settings.write_text("{}")
        self.keymap.write_text("[42]")
        result = self.configure("bad", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.settings.read_text(), "{}")
        self.assertEqual(self.keymap.read_text(), "[42]")
        self.assertEqual(list(self.config.glob("*.bak-*")), [])


if __name__ == "__main__":
    unittest.main()
