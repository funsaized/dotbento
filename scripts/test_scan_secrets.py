"""Check Tavily detection without echoing credential-shaped test data."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class SecretScannerTests(unittest.TestCase):
    def test_tavily_detection_redacts_tree_and_staged_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            scanner = root / "scripts" / "scan-secrets.sh"
            shutil.copy2(Path(__file__).with_name("scan-secrets.sh"), scanner)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            # Generated synthetic data, never an actual credential.
            token = "tvly-" + "test-" + "a" * 32
            (root / "accidental.json").write_text(token)
            subprocess.run(["git", "add", "accidental.json"], cwd=root, check=True)
            for args in ([], ["--staged"]):
                result = subprocess.run(
                    ["bash", str(scanner), *args], capture_output=True, text=True
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("accidental.json", result.stdout)
                self.assertNotIn(token, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
