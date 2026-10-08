"""Exercise settings merging against real temporary files."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "configure_pi", Path(__file__).with_name("configure-pi.py")
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
DEFAULTS = Path(__file__).resolve().parents[1] / "pi" / "settings.json"


class ConfigurePiTests(unittest.TestCase):
    def test_merge_preserves_local_settings_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "settings.json"
            original = {
                "theme": "local-theme",
                "deviceId": "local-id",
                "packages": ["git:example.com/local/package"],
                "defaultProvider": "anthropic",
                "enabledModels": ["anthropic/*"],
                "modelThinkingLevels": {"anthropic/local": "high"},
            }
            destination.write_text(json.dumps(original))
            MODULE.configure(DEFAULTS, destination, "first")
            merged = json.loads(destination.read_text())
            for key in ("theme", "deviceId", "packages"):
                self.assertEqual(merged[key], original[key])
            self.assertEqual(merged["defaultProvider"], "openai")
            self.assertEqual(merged["defaultTools"], ["+codemode"])
            self.assertEqual(merged["modelThinkingLevels"]["anthropic/local"], "high")
            self.assertEqual(merged["modelThinkingLevels"]["openai/gpt-6.1-sol"], "low")
            self.assertEqual(merged["modelThinkingLevels"]["openai/gpt-6-astra"], "medium")
            self.assertEqual(merged["modelThinkingLevels"]["deepseek/deepseek-flash"], "max")
            self.assertIn("openai/gpt-6-astra:medium", merged["enabledModels"])
            self.assertIn("deepseek/deepseek-flash:max", merged["enabledModels"])
            self.assertEqual(len(merged["enabledModels"]), 4)
            backup = destination.with_name("settings.json.bak-first")
            self.assertEqual(json.loads(backup.read_text()), original)
            MODULE.configure(DEFAULTS, destination, "second")
            self.assertFalse(destination.with_name("settings.json.bak-second").exists())

    def test_dry_run_leaves_existing_and_missing_settings_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "settings.json"
            MODULE.configure(DEFAULTS, destination, "dry", True)
            self.assertFalse(destination.exists())
            destination.write_text('{"theme":"local"}')
            MODULE.configure(DEFAULTS, destination, "dry", True)
            self.assertEqual(destination.read_text(), '{"theme":"local"}')
            self.assertEqual(list(Path(directory).iterdir()), [destination])

    def test_web_defaults_preserve_private_credentials_and_nested_preferences(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "web-search.json"
            original = {
                "tavilyApiKey": "test-only-placeholder",
                "provider": "exa",
                "fetchRouting": {"providers": ["jina"], "localPreference": True},
            }
            destination.write_text(json.dumps(original))
            MODULE.configure(DEFAULTS.with_name("web-search.json"), destination, "web")
            merged = json.loads(destination.read_text())
            self.assertEqual(merged["tavilyApiKey"], original["tavilyApiKey"])
            self.assertEqual(merged["provider"], "tavily")
            self.assertEqual(merged["webSearch"]["allowedProviders"], ["tavily"])
            self.assertEqual(merged["fetchRouting"]["providers"], ["http"])
            self.assertTrue(merged["fetchRouting"]["localPreference"])
            self.assertEqual(destination.stat().st_mode & 0o777, 0o600)
            backup = destination.with_name("web-search.json.bak-web")
            self.assertEqual(backup.stat().st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(backup.read_text()), original)

    def test_new_settings_and_invalid_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "agent" / "settings.json"
            MODULE.configure(DEFAULTS, destination, "new")
            self.assertEqual(json.loads(destination.read_text()), json.loads(DEFAULTS.read_text()))
            destination.write_text("not json")
            with self.assertRaises(json.JSONDecodeError):
                MODULE.configure(DEFAULTS, destination, "invalid")
            self.assertEqual(destination.read_text(), "not json")
            self.assertFalse(destination.with_name("settings.json.bak-invalid").exists())


if __name__ == "__main__":
    unittest.main()
