from __future__ import annotations

import json
import os
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


def run_cli(
    *args: str,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        env=env,
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

    def test_init_does_not_persist_environment_username(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "private-owner.md"
            environment = {**os.environ, "USER": "personal-system-login"}
            created = run_cli("init", str(target), "--title", "Private owner", env=environment)
            self.assertEqual(created.returncode, 0, created.stderr)
            source = target.read_text(encoding="utf-8")
            self.assertIn('owner: "unassigned"', source)
            self.assertNotIn("personal-system-login", source)

    def test_ready_gate_requires_explicit_owner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "unassigned-owner.md"
            text = DOGFOOD.read_text(encoding="utf-8").replace("owner: dimidotdev", 'owner: " unassigned "')
            target.write_text(text, encoding="utf-8")
            result = run_cli("check", str(target), "--gate", "ready", "--format", "json")
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertIn("OWNER001", {finding["code"] for finding in payload["findings"]})

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

    def test_verified_gate_requires_disposition_for_should_requirements(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "should-gap.md"
            text = DOGFOOD.read_text(encoding="utf-8")
            text = text.replace("- REQ-012 | must-not |", "- REQ-012 | should |")
            text = text.replace("| REQ-012 | AC-012 | TEST-012 | passed |\n", "")
            target.write_text(text, encoding="utf-8")
            result = run_cli("check", str(target), "--gate", "verified", "--format", "json")
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertIn("GATE005", {finding["code"] for finding in payload["findings"]})
            trace = run_cli("trace", str(target), "--format", "json")
            self.assertEqual(trace.returncode, 1)
            self.assertFalse(json.loads(trace.stdout)["complete"])

    def test_not_applicable_requires_decision_explanation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "not-applicable.md"
            text = DOGFOOD.read_text(encoding="utf-8")
            text = text.replace("- REQ-012 | must-not |", "- REQ-012 | should |")
            text = text.replace(
                "| REQ-012 | AC-012 | TEST-012 | passed |",
                "| REQ-012 | AC-012 | TEST-012 | not-applicable |",
            )
            target.write_text(text, encoding="utf-8")
            rejected = run_cli("check", str(target), "--gate", "verified", "--format", "json")
            self.assertEqual(rejected.returncode, 1)
            payload = json.loads(rejected.stdout)
            self.assertIn("TRACE008", {finding["code"] for finding in payload["findings"]})

            bare_decision = "- DEC-005 | REQ-012\n"
            source = target.read_text(encoding="utf-8").replace(
                "## Open Questions\n",
                f"{bare_decision}\n## Open Questions\n",
            )
            target.write_text(source, encoding="utf-8")
            still_rejected = run_cli("check", str(target), "--gate", "verified", "--format", "json")
            self.assertEqual(still_rejected.returncode, 1)
            payload = json.loads(still_rejected.stdout)
            self.assertIn("TRACE008", {finding["code"] for finding in payload["findings"]})

            empty_rationale = "- DEC-005 | req-012 | rationale: | affects: REQ-012\n"
            source = target.read_text(encoding="utf-8").replace(bare_decision, empty_rationale)
            target.write_text(source, encoding="utf-8")
            still_rejected = run_cli("check", str(target), "--gate", "verified", "--format", "json")
            self.assertEqual(still_rejected.returncode, 1)
            payload = json.loads(still_rejected.stdout)
            self.assertIn("TRACE008", {finding["code"] for finding in payload["findings"]})

            punctuation_rationale = "- DEC-005 | req-012 | rationale: - | affects: REQ-012\n"
            source = target.read_text(encoding="utf-8").replace(empty_rationale, punctuation_rationale)
            target.write_text(source, encoding="utf-8")
            still_rejected = run_cli("check", str(target), "--gate", "verified", "--format", "json")
            self.assertEqual(still_rejected.returncode, 1)
            payload = json.loads(still_rejected.stdout)
            self.assertIn("TRACE008", {finding["code"] for finding in payload["findings"]})

            decision = (
                "- DEC-005 | req-012 is not applicable to this verification because its advisory "
                "behavior was intentionally excluded. | rationale: approved scope boundary\n"
            )
            source = target.read_text(encoding="utf-8").replace(punctuation_rationale, decision)
            target.write_text(source, encoding="utf-8")
            accepted = run_cli("check", str(target), "--gate", "verified")
            self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)

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
        evidence_cases = (
            "review record dated 2026-07-29",
            "security due diligence report 2026-07-31",
            "https://example.com/reviews/security-001",
        )
        for evidence in evidence_cases:
            with self.subTest(evidence=evidence):
                with tempfile.TemporaryDirectory() as directory:
                    target = Path(directory) / "critical-reviewed.md"
                    text = DOGFOOD.read_text(encoding="utf-8").replace("profile: standard", "profile: critical")
                    review = (
                        "- REVIEW-001 | security | passed | reviewer: independent-reviewer | "
                        f"evidence: {evidence}\n\n"
                    )
                    text = text.replace("## Decisions\n", f"{review}## Decisions\n")
                    target.write_text(text, encoding="utf-8")
                    result = run_cli("check", str(target), "--gate", "ready")
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_critical_ready_gate_rejects_self_review_without_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "critical-self-reviewed.md"
            text = DOGFOOD.read_text(encoding="utf-8").replace("profile: standard", "profile: critical")
            review = "- REVIEW-001 | security | passed | reviewer: self | evidence: none\n\n"
            text = text.replace("## Decisions\n", f"{review}## Decisions\n")
            target.write_text(text, encoding="utf-8")
            result = run_cli("check", str(target), "--gate", "ready", "--format", "json")
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            codes = {finding["code"] for finding in payload["findings"]}
            self.assertTrue({"CRIT005", "REVIEW003", "REVIEW004"}.issubset(codes))

    def test_critical_review_rejects_owner_placeholder_and_nonconcrete_evidence(self) -> None:
        cases = (
            ("dimidotdev", "review record dated 2026-07-31", "REVIEW003"),
            ('"dimidotdev"', "review record dated 2026-07-31", "REVIEW003"),
            ("unassigned", "review record dated 2026-07-31", "REVIEW003"),
            ("autor", "registro de revisão de 2026-07-31", "REVIEW003"),
            ("eu", "registro de revisão de 2026-07-31", "REVIEW003"),
            ("yo", "registro de revisión de 2026-07-31", "REVIEW003"),
            ("independent-reviewer", "N/A — review not recorded", "REVIEW004"),
            ("independent-reviewer", "none provided", "REVIEW004"),
            ("independent-reviewer", '"none"', "REVIEW004"),
            ("independent-reviewer", "pending", "REVIEW004"),
            ("independent-reviewer", "planned", "REVIEW004"),
            ("independent-reviewer", "review planned for 2026-08-01", "REVIEW004"),
            ("independent-reviewer", "review planned: https://example.com/review-plan", "REVIEW004"),
            (
                "independent-reviewer",
                "review of the authentication migration is planned: https://example.com/review-plan",
                "REVIEW004",
            ),
            ("independent-reviewer", "revisão pendente em 2026-08-01", "REVIEW004"),
            ("independent-reviewer", "revisión planificada para 2026-08-01", "REVIEW004"),
            ("independent-reviewer", "review required by 2026-08-01", "REVIEW004"),
            ("independent-reviewer", "2026-08-01", "REVIEW004"),
        )
        for reviewer, evidence, expected_code in cases:
            with self.subTest(reviewer=reviewer, evidence=evidence):
                with tempfile.TemporaryDirectory() as directory:
                    target = Path(directory) / "critical-invalid-review.md"
                    text = DOGFOOD.read_text(encoding="utf-8").replace("profile: standard", "profile: critical")
                    review = (
                        f"- REVIEW-001 | security | passed | reviewer: {reviewer} | "
                        f"evidence: {evidence}\n\n"
                    )
                    text = text.replace("## Decisions\n", f"{review}## Decisions\n")
                    target.write_text(text, encoding="utf-8")
                    result = run_cli("check", str(target), "--gate", "ready", "--format", "json")
                    self.assertEqual(result.returncode, 1)
                    payload = json.loads(result.stdout)
                    self.assertIn(expected_code, {finding["code"] for finding in payload["findings"]})

    def test_localized_portuguese_critical_spec_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "critical-portuguese.md"
            text = DOGFOOD.read_text(encoding="utf-8").replace("profile: standard", "profile: critical")
            text = text.replace("Given ", "Dado ").replace(", when ", ", quando ").replace(", then ", ", então ")
            text = text.replace("trust boundaries", "fronteiras de confiança")
            text = text.replace("Abuse", "Abuso").replace("authorization", "autorização")
            text = text.replace("retention", "retenção")
            text = text.replace("Stop conditions:", "Condições de parada:")
            text = text.replace(
                "Rollback or forward recovery:",
                "Reversão ou recuperação progressiva:",
            )
            review = (
                "- REVIEW-001 | security | passed | reviewer: revisor-independente | "
                "evidence: registro de revisão de 2026-07-31\n\n"
            )
            text = text.replace("## Decisions\n", f"{review}## Decisions\n")
            target.write_text(text, encoding="utf-8")
            result = run_cli("check", str(target), "--gate", "ready")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_localized_spanish_critical_spec_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "critical-spanish.md"
            text = DOGFOOD.read_text(encoding="utf-8").replace("profile: standard", "profile: critical")
            text = text.replace("Given ", "Dado ").replace(", when ", ", cuando ").replace(", then ", ", entonces ")
            text = text.replace("trust boundaries", "límites de confianza")
            text = text.replace("Abuse", "Abuso").replace("authorization", "autorización")
            text = text.replace("retention", "retención")
            text = text.replace("Stop conditions:", "Condiciones de detención:")
            text = text.replace(
                "Rollback or forward recovery:",
                "Reversión o recuperación progresiva:",
            )
            review = (
                "- REVIEW-001 | security | passed | reviewer: revisor-independiente | "
                "evidence: registro de revisión de 2026-07-31\n\n"
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
