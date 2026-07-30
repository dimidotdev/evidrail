from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skill" / "spec-driven-development" / "scripts" / "evidrail.py"
DOGFOOD = ROOT / "specs" / "evidrail-v1.md"
INVALID = ROOT / "tests" / "fixtures" / "invalid-spec.md"
VALID_LIGHT = ROOT / "tests" / "fixtures" / "valid-light-spec.md"


def run_cli(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class EvidrailCliTests(unittest.TestCase):
    def test_compact_light_spec_passes_ready_gate(self) -> None:
        result = run_cli("check", str(VALID_LIGHT), "--gate", "ready")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_dogfood_spec_passes_ready_gate(self) -> None:
        result = run_cli("check", str(DOGFOOD), "--gate", "ready")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)
        self.assertIn("12 requirement(s)", result.stdout)

    def test_json_output_is_one_machine_readable_document(self) -> None:
        result = run_cli("check", str(DOGFOOD), "--gate", "ready", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual(payload["summary"]["errors"], 0)
        self.assertFalse(Path(payload["path"]).is_absolute())

    def test_sarif_output_is_valid_and_deterministic(self) -> None:
        first = run_cli("check", str(INVALID), "--gate", "ready", "--format", "sarif")
        second = run_cli("check", str(INVALID), "--gate", "ready", "--format", "sarif")
        self.assertEqual(first.returncode, 1)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        self.assertEqual(payload["version"], "2.1.0")
        self.assertEqual(payload["runs"][0]["tool"]["driver"]["name"], "Evidrail")
        self.assertGreater(len(payload["runs"][0]["results"]), 0)

    def test_invalid_spec_reports_structural_and_semantic_findings(self) -> None:
        result = run_cli("check", str(INVALID), "--gate", "ready", "--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        codes = {finding["code"] for finding in payload["findings"]}
        self.assertTrue(
            {"CONTENT001", "CONTENT002", "ID001", "AC003", "TRACE003", "TRACE004", "TRACE006", "QUESTION003"}.issubset(codes)
        )

    def test_init_creates_template_and_refuses_implicit_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "change.md"
            created = run_cli(
                "init",
                str(target),
                "--title",
                "Bounded change",
                "--profile",
                "light",
                "--mode",
                "specify",
                "--owner",
                "test-team",
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            original = target.read_text(encoding="utf-8")
            self.assertIn('title: "Bounded change"', original)
            self.assertIn("profile: light", original)
            self.assertIn("mode: specify", original)

            refused = run_cli("init", str(target), "--title", "Replacement")
            self.assertEqual(refused.returncode, 3)
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_generated_draft_can_be_checked_before_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "draft.md"
            created = run_cli("init", str(target), "--title", "Draft contract")
            self.assertEqual(created.returncode, 0, created.stderr)
            checked = run_cli("check", str(target), "--gate", "draft", "--format", "json")
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            payload = json.loads(checked.stdout)
            self.assertGreater(payload["summary"]["warnings"], 0)

    def test_verified_gate_requires_passed_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "verified.md"
            verified_text = DOGFOOD.read_text(encoding="utf-8")
            target.write_text(verified_text.replace("| passed |", "| planned |"), encoding="utf-8")
            blocked = run_cli("check", str(target), "--gate", "verified")
            self.assertEqual(blocked.returncode, 1)
            self.assertIn("GATE003", blocked.stdout)

            target.write_text(
                target.read_text(encoding="utf-8").replace("| planned |", "| passed |"),
                encoding="utf-8",
            )
            passed = run_cli("check", str(target), "--gate", "verified")
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

    def test_trace_fails_when_normative_coverage_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "trace-gap.md"
            text = DOGFOOD.read_text(encoding="utf-8")
            text = text.replace("| REQ-012 | AC-012 | TEST-012 | passed |\n", "")
            target.write_text(text, encoding="utf-8")
            result = run_cli("trace", str(target), "--format", "json")
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["complete"])
            row = next(item for item in payload["matrix"] if item["requirement"] == "REQ-012")
            self.assertEqual(row["verification"], [])

    def test_critical_ready_gate_treats_warnings_as_failures(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "critical.md"
            text = DOGFOOD.read_text(encoding="utf-8").replace("profile: standard", "profile: critical")
            target.write_text(text, encoding="utf-8")
            result = run_cli("check", str(target), "--gate", "ready", "--format", "json")
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["passed"])
            self.assertIn("CRIT005", {finding["code"] for finding in payload["findings"]})

    def test_structured_passed_review_satisfies_critical_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "critical-reviewed.md"
            text = DOGFOOD.read_text(encoding="utf-8").replace("profile: standard", "profile: critical")
            review = (
                "- REVIEW-001 | security | passed | reviewer: independent-reviewer | "
                "evidence: review record dated 2026-07-29\n\n"
            )
            text = text.replace("## Decisions\n", f"{review}## Decisions\n")
            target.write_text(text, encoding="utf-8")
            result = run_cli("check", str(target), "--gate", "ready")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_light_init_uses_micro_spec_and_normalizes_prefixed_filename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "spec-route-shift.md"
            result = run_cli(
                "init",
                str(target),
                "--title",
                "Route shift",
                "--profile",
                "light",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            source = target.read_text(encoding="utf-8")
            self.assertIn("spec: SPEC-ROUTE-SHIFT-0001", source)
            self.assertNotIn("## Product and Design", source)
            self.assertNotIn("## Rollout and Rollback", source)

    def test_init_rejects_invalid_identity_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "invalid.md"
            result = run_cli(
                "init",
                str(target),
                "--title",
                "Valid title",
                "--spec-id",
                "invalid-id",
            )
            self.assertEqual(result.returncode, 2)
            self.assertFalse(target.exists())

    def test_machine_output_does_not_expose_absolute_input_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "portable.md"
            target.write_text(DOGFOOD.read_text(encoding="utf-8"), encoding="utf-8")
            result = run_cli("check", str(target), "--gate", "ready", "--format", "json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["path"], "portable.md")

    def test_markdown_examples_do_not_define_structure_or_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "examples.md"
            text = DOGFOOD.read_text(encoding="utf-8")
            example = """```markdown
## Fake section
- REQ-001 | must | TODO inside a quoted example.
```

"""
            text = text.replace("## Problem\n", f"{example}## Problem\n")
            target.write_text(text, encoding="utf-8")
            result = run_cli("check", str(target), "--gate", "ready")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_utf8_bom_and_crlf_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "portable.md"
            text = DOGFOOD.read_text(encoding="utf-8").replace("\n", "\r\n")
            target.write_text(f"\ufeff{text}", encoding="utf-8")
            result = run_cli("check", str(target), "--gate", "ready")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
