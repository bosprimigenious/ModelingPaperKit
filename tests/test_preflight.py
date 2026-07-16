#!/usr/bin/env python3
"""Regression tests for the integrated CUMCM preflight runner."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


class PreflightTest(unittest.TestCase):
    def run_preflight(self, *args: str) -> dict[str, object]:
        proc = subprocess.run(
            [sys.executable, "scripts/preflight.py", "--target", "cumcm", "--format", "json", *args],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        return json.loads(proc.stdout)

    def test_default_preflight_allows_template_placeholders(self) -> None:
        result = self.run_preflight()

        self.assertEqual(result["tool"], "preflight")
        self.assertEqual(result["target"], "cumcm")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["summary"]["critical"], 0)
        self.assertEqual(result["summary"]["warning"], 0)

    def test_strict_placeholders_reports_warning_without_failing(self) -> None:
        result = self.run_preflight("--strict-placeholders", "--skip-skills")

        self.assertEqual(result["summary"]["critical"], 0)
        self.assertGreaterEqual(result["summary"]["warning"], 1)
        self.assertEqual(result["status"], "warning")
        codes = {finding["code"] for finding in result["findings"]}
        self.assertIn("missing_figplot_asset", codes)

    def test_text_output_hides_info_by_default(self) -> None:
        proc = subprocess.run(
            [sys.executable, "scripts/preflight.py", "--target", "cumcm"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        self.assertIn("info findings hidden:", proc.stdout)
        self.assertNotIn("[info]", proc.stdout)

    def test_text_output_can_show_info(self) -> None:
        proc = subprocess.run(
            [sys.executable, "scripts/preflight.py", "--target", "cumcm", "--show-info"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        self.assertIn("[info]", proc.stdout)


if __name__ == "__main__":
    unittest.main()
