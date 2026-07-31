#!/usr/bin/env python3
"""Dependency-free validator and traceability helper for Evidrail specs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_IO = 3
VERSION = "0.1.0"
MAX_SPEC_BYTES = 5_000_000

SEVERITY_ORDER = {"error": 0, "warning": 1, "note": 2}
VALID_STATUSES = {"draft", "ready", "implemented", "verified", "superseded"}
VALID_PROFILES = {"light", "standard", "critical"}
VALID_MODES = {"specify", "deliver", "audit"}
VALID_LEVELS = {"must", "must-not", "should", "may"}
VALID_TRACE_STATUSES = {"planned", "passed", "failed", "blocked", "not-applicable"}
VALID_QUESTION_STATUSES = {"blocking", "non-blocking", "deferred", "resolved"}

CANONICAL_SECTIONS = [
    "Context and Evidence",
    "Problem",
    "Outcomes",
    "Non-goals",
    "Users and Scenarios",
    "Current Behavior",
    "Proposed Behavior",
    "Requirements",
    "Acceptance Criteria",
    "Product and Design",
    "Security and Privacy",
    "Data and Interfaces",
    "Failure Modes and Recovery",
    "Observability",
    "Rollout and Rollback",
    "Verification and Traceability",
    "Decisions",
    "Open Questions",
]

PROFILE_SECTIONS = {
    "light": [
        "Context and Evidence",
        "Problem",
        "Outcomes",
        "Non-goals",
        "Current Behavior",
        "Proposed Behavior",
        "Requirements",
        "Acceptance Criteria",
        "Security and Privacy",
        "Verification and Traceability",
        "Decisions",
        "Open Questions",
    ],
    "standard": CANONICAL_SECTIONS,
    "critical": CANONICAL_SECTIONS,
}

METADATA_KEYS = {"spec", "title", "status", "profile", "mode", "owner", "created", "updated"}
REQUIREMENT_RE = re.compile(
    r"^\s*-\s+(REQ-\d{3,})\s*\|\s*(must-not|must|should|may)\s*\|\s*(.+?)\s*$",
    re.IGNORECASE,
)
ACCEPTANCE_RE = re.compile(
    r"^\s*-\s+(AC-\d{3,})\s*\|\s*(REQ-\d{3,})\s*\|\s*(.+?)\s*$",
    re.IGNORECASE,
)
QUESTION_RE = re.compile(
    r"^\s*-\s+(Q-\d{3,})\s*\|\s*([a-z-]+)\s*\|\s*(.+?)\s*$",
    re.IGNORECASE,
)
REVIEW_RE = re.compile(
    r"^\s*-\s+(REVIEW-\d{3,})\s*\|\s*(general|security|privacy|design|verification)\s*\|\s*"
    r"(planned|passed|failed|blocked)\s*\|\s*reviewer:\s*([^|]+?)\s*\|\s*evidence:\s*(.+?)\s*$",
    re.IGNORECASE,
)
DEFINITION_RE = re.compile(
    r"^\s*-\s+((?:EVD|ASM|REQ|AC|DEC|Q|REVIEW)-\d{3,})\b", re.IGNORECASE
)
PLACEHOLDER_RE = re.compile(
    r"\b(?:TODO|TBD|TBC|FIXME|XXX)\b|\?\?\?|YYYY-MM-DD|\{\{[^}\n]+\}\}|"
    r"<(?:fill|insert|describe|title|owner|date|value|text|here)[^>\n]*>|lorem ipsum",
    re.IGNORECASE,
)
AMBIGUOUS_RE = re.compile(
    r"\b(?:fast|quick|easy|simple|seamless|secure|safe|robust|scalable|intuitive|reasonable|"
    r"performant|user-friendly|best[- ]practice|rápid[oa]|fácil|simples|segur[oa]|robust[oa]|"
    r"escalável|intuitiv[oa]|quickly|soon|as needed|as appropriate|when possible|etc)\b|and/or",
    re.IGNORECASE,
)

ACCEPTANCE_KEYWORD_SETS = (
    (r"\bgiven\b", r"\bwhen\b", r"\bthen\b"),
    (r"\b(?:dado|dada|dados|dadas)\b", r"\bquando\b", r"\b(?:então|entao)\b"),
    (r"\b(?:dado|dada|dados|dadas)\b", r"\bcuando\b", r"\bentonces\b"),
)

RISK_SECTION_CHECKS = (
    (
        r"\b(?:rollback|roll back|revert|reversion|recovery|reversão|reversao|recuperação|"
        r"recuperacao|reversión|reversion|recuperación|recuperacion)\b",
        "RISK001",
        "rollback or forward-recovery path",
    ),
    (
        r"\b(?:stop|halt|pause|parada|parar|interrupção|interrupcao|detener|detención|detencion)\b",
        "RISK002",
        "rollout stop condition",
    ),
)

CRITICAL_SECTION_CHECKS = (
    (
        "Security and Privacy",
        r"trust\s+boundar|fronteira(?:s)?\s+de\s+confiança|fronteira(?:s)?\s+de\s+confianca|"
        r"l[ií]mite(?:s)?\s+de\s+confianza",
        "CRIT001",
        "trust boundaries",
    ),
    (
        "Security and Privacy",
        r"\b(?:abuse|misuse|abuso|uso\s+indevido|mal\s+uso)\b",
        "CRIT002",
        "abuse or misuse cases",
    ),
    (
        "Security and Privacy",
        r"authoriz|autoriza(?:ção|cao)|autorizaci[oó]n",
        "CRIT003",
        "authorization decisions",
    ),
    (
        "Security and Privacy",
        r"retention|classification|reten(?:ção|cao)|classifica(?:ção|cao)|retenci[oó]n|"
        r"clasificaci[oó]n",
        "CRIT004",
        "data classification or retention",
    ),
)

NON_INDEPENDENT_REVIEWERS = {
    "self",
    "myself",
    "author",
    "spec author",
    "owner",
    "unassigned",
    "eu",
    "autor",
    "autora",
    "próprio",
    "proprio",
    "própria",
    "propria",
    "yo",
    "mismo",
    "misma",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    line: int = 1
    column: int = 1


@dataclass(frozen=True)
class Requirement:
    identifier: str
    level: str
    text: str
    line: int


@dataclass(frozen=True)
class Acceptance:
    identifier: str
    requirement: str
    text: str
    line: int


@dataclass(frozen=True)
class TraceRow:
    requirement: str
    acceptance: str
    verification: str
    status: str
    line: int


@dataclass(frozen=True)
class ReviewRecord:
    identifier: str
    scope: str
    status: str
    reviewer: str
    evidence: str
    line: int


@dataclass
class Document:
    path: Path
    display_path: str
    lines: list[str]
    metadata: dict[str, str]
    metadata_lines: dict[str, int]
    sections: dict[str, list[tuple[int, str]]]
    section_lines: dict[str, int]
    h1: list[tuple[int, str]]
    parse_findings: list[Finding]


def _strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        if value[0] == '"':
            try:
                parsed = json.loads(value)
                return parsed if isinstance(parsed, str) else value
            except json.JSONDecodeError:
                return value[1:-1]
        return value[1:-1].replace("''", "'")
    return value


def _markdown_prose(lines: Sequence[str], body_start: int) -> list[str]:
    """Remove fenced/indented code and HTML comments from lintable Markdown."""
    result = list(lines[:body_start]) + [""] * max(0, len(lines) - body_start)
    fence_char: str | None = None
    fence_length = 0
    in_comment = False

    for index in range(body_start, len(lines)):
        raw = lines[index]
        cursor = 0
        visible: list[str] = []
        while cursor < len(raw):
            if in_comment:
                closing = raw.find("-->", cursor)
                if closing < 0:
                    cursor = len(raw)
                    break
                in_comment = False
                cursor = closing + 3
                continue
            opening = raw.find("<!--", cursor)
            if opening < 0:
                visible.append(raw[cursor:])
                break
            visible.append(raw[cursor:opening])
            in_comment = True
            cursor = opening + 4
        line = "".join(visible)

        if fence_char is not None:
            closing_match = re.match(r"^\s{0,3}([`~]{3,})\s*$", line)
            if (
                closing_match
                and closing_match.group(1)[0] == fence_char
                and len(closing_match.group(1)) >= fence_length
            ):
                fence_char = None
                fence_length = 0
            continue

        opening_match = re.match(r"^\s{0,3}([`~]{3,})(?:\s*.*)?$", line)
        if opening_match:
            fence = opening_match.group(1)
            fence_char = fence[0]
            fence_length = len(fence)
            continue
        if line.startswith("    ") or line.startswith("\t"):
            continue
        result[index] = line
    return result


def parse_document(path: Path, display_path: str | None = None) -> Document:
    try:
        if not path.is_file():
            raise OSError("path is not a regular file")
        if path.stat().st_size > MAX_SPEC_BYTES:
            raise OSError(f"file exceeds the {MAX_SPEC_BYTES}-byte limit")
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise IOError(f"cannot read {path}: {exc}") from exc

    lines = text.splitlines()
    findings: list[Finding] = []
    metadata: dict[str, str] = {}
    metadata_lines: dict[str, int] = {}
    body_start = 0

    if not lines or lines[0].strip() != "---":
        findings.append(Finding("error", "META001", "frontmatter must start on line 1"))
    else:
        closing = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
        if closing is None:
            findings.append(Finding("error", "META002", "frontmatter is missing its closing delimiter"))
            body_start = len(lines)
        else:
            body_start = closing + 1
            for index in range(1, closing):
                raw = lines[index]
                if not raw.strip():
                    continue
                match = re.match(r"^([a-z][a-z0-9_-]*):\s*(.*?)\s*$", raw)
                if not match:
                    findings.append(
                        Finding("error", "META003", "frontmatter supports only scalar key: value entries", index + 1)
                    )
                    continue
                key, raw_value = match.groups()
                if key in metadata:
                    findings.append(Finding("error", "META004", f"duplicate metadata key: {key}", index + 1))
                    continue
                metadata[key] = _strip_scalar(raw_value)
                metadata_lines[key] = index + 1

    prose_lines = _markdown_prose(lines, body_start)
    sections: dict[str, list[tuple[int, str]]] = {}
    section_lines: dict[str, int] = {}
    h1: list[tuple[int, str]] = []
    current: str | None = None

    for index in range(body_start, len(lines)):
        raw = prose_lines[index]
        h2_match = re.match(r"^##\s+(.+?)\s*$", raw)
        if h2_match:
            name = h2_match.group(1)
            if name in sections:
                findings.append(Finding("error", "STRUCT003", f"duplicate section: {name}", index + 1))
            else:
                sections[name] = []
                section_lines[name] = index + 1
            current = name
            continue
        h1_match = re.match(r"^#\s+(.+?)\s*$", raw)
        if h1_match:
            h1.append((index + 1, h1_match.group(1)))
        if current is not None:
            sections[current].append((index + 1, raw))

    return Document(
        path=path,
        display_path=display_path or path.as_posix(),
        lines=lines,
        metadata=metadata,
        metadata_lines=metadata_lines,
        sections=sections,
        section_lines=section_lines,
        h1=h1,
        parse_findings=findings,
    )


def section_text(document: Document, section: str) -> str:
    return "\n".join(raw for _, raw in document.sections.get(section, [])).strip()


def _has_acceptance_structure(text: str) -> bool:
    return any(
        all(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)
        for patterns in ACCEPTANCE_KEYWORD_SETS
    )


def _normalize_claim(value: str) -> str:
    value = value.strip()
    while len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    return " ".join(value.casefold().split())


def _decision_explains_requirement(document: Document, requirement: str) -> bool:
    blocks: list[list[str]] = []
    current: list[str] = []
    for _, raw in document.sections.get("Decisions", []):
        if re.match(r"^\s*-\s+DEC-\d{3,}\b", raw, re.IGNORECASE):
            if current:
                blocks.append(current)
            current = [raw]
        elif current:
            current.append(raw)
    if current:
        blocks.append(current)
    rationale_pattern = (
        r"\b(?:rationale|justificativa|raz[oó]n|motivo)\s*:\s*"
        r"[^|\n]*[^\W_][^|\n]*(?:\||$)"
    )
    return any(
        re.search(rf"\b{re.escape(requirement)}\b", text, re.IGNORECASE)
        and re.search(rationale_pattern, text, re.IGNORECASE)
        for text in ("\n".join(block) for block in blocks)
    )


def _review_is_independent(record: ReviewRecord, owner: str) -> bool:
    reviewer = _normalize_claim(record.reviewer)
    normalized_owner = _normalize_claim(owner)
    return reviewer not in NON_INDEPENDENT_REVIEWERS and (
        not normalized_owner or reviewer != normalized_owner
    )


def _review_has_evidence(record: ReviewRecord) -> bool:
    evidence = _normalize_claim(record.evidence)
    if re.match(
        r"^(?:none\b|n\s*/?\s*a\b|not\s+applicable\b|no\s+evidence\b|not\s+recorded\b|"
        r"unavailable\b)",
        evidence,
    ):
        return False
    has_url = bool(re.search(r"https?://\S+", evidence))
    prose_without_urls = re.sub(r"https?://\S+", "", evidence)
    subject = r"review|record|report|artifact|revis[aã]o|revisi[oó]n|registro|relat[oó]rio|informe|artefato"
    unresolved = (
        r"pending|planned|scheduled|required|pendente|planejad[oa]|programad[oa]|"
        r"obrigat[oó]ri[oa]|requerid[oa]|pendiente|planificad[oa]"
    )
    contextual_status = (
        rf"(?:\b(?:{subject})\b[^\n.!?;]{{0,200}}\b(?:{unresolved})\b)|"
        rf"(?:\b(?:{unresolved})\b[^\n.!?;]{{0,200}}\b(?:{subject})\b)|"
        r"(?:\b(?:review|revis[aã]o|revisi[oó]n)\s+(?:due|future|incomplete|awaiting|"
        r"futur[oa]|incomplet[oa]|aguardando)\b)|"
        r"(?:\b(?:due|future|incomplete|awaiting|futur[oa]|incomplet[oa]|aguardando)\s+"
        r"(?:review|revis[aã]o|revisi[oó]n)\b)"
    )
    if re.search(contextual_status, prose_without_urls):
        return False
    if has_url:
        return True
    artifact_pattern = (
        r"\b(?:review\s+(?:record|report|artifact)|(?:completed|passed|approved)\s+review|"
        r"record|report|artifact|registro|relat[oó]rio|informe|artefato)\b"
    )
    if not re.search(artifact_pattern, evidence):
        return False
    for candidate in re.findall(r"\b\d{4}-\d{2}-\d{2}\b", evidence):
        try:
            dt.date.fromisoformat(candidate)
            return True
        except ValueError:
            continue
    return False


def _definition_duplicates(document: Document) -> list[Finding]:
    definitions: dict[str, int] = {}
    findings: list[Finding] = []
    relevant_sections = {
        "Context and Evidence",
        "Requirements",
        "Acceptance Criteria",
        "Verification and Traceability",
        "Decisions",
        "Open Questions",
    }
    for section in relevant_sections:
        for line, raw in document.sections.get(section, []):
            match = DEFINITION_RE.match(raw)
            if not match:
                continue
            identifier = match.group(1).upper()
            if identifier in definitions:
                findings.append(
                    Finding(
                        "error",
                        "ID001",
                        f"duplicate definition {identifier}; first defined on line {definitions[identifier]}",
                        line,
                    )
                )
            else:
                definitions[identifier] = line
    return findings


def parse_requirements(document: Document) -> tuple[list[Requirement], list[Finding]]:
    requirements: list[Requirement] = []
    findings: list[Finding] = []
    for line, raw in document.sections.get("Requirements", []):
        if not raw.strip() or raw.lstrip().startswith("<!--"):
            continue
        match = REQUIREMENT_RE.match(raw)
        if match:
            identifier, level, text = match.groups()
            requirements.append(Requirement(identifier.upper(), level.lower(), text.strip(), line))
        elif re.search(r"\bREQ-\d+\b", raw, re.IGNORECASE):
            findings.append(
                Finding(
                    "error",
                    "REQ001",
                    "malformed requirement; expected '- REQ-001 | must | observable behavior'",
                    line,
                )
            )
    return requirements, findings


def parse_acceptance(document: Document) -> tuple[list[Acceptance], list[Finding]]:
    acceptance: list[Acceptance] = []
    findings: list[Finding] = []
    for line, raw in document.sections.get("Acceptance Criteria", []):
        if not raw.strip() or raw.lstrip().startswith("<!--"):
            continue
        match = ACCEPTANCE_RE.match(raw)
        if match:
            identifier, requirement, text = match.groups()
            acceptance.append(Acceptance(identifier.upper(), requirement.upper(), text.strip(), line))
        elif re.search(r"\bAC-\d+\b", raw, re.IGNORECASE):
            findings.append(
                Finding(
                    "error",
                    "AC001",
                    "malformed acceptance criterion; expected '- AC-001 | REQ-001 | Given ..., when ..., then ...'",
                    line,
                )
            )
    return acceptance, findings


def parse_trace(document: Document) -> tuple[list[TraceRow], list[Finding]]:
    rows: list[TraceRow] = []
    findings: list[Finding] = []
    section = document.sections.get("Verification and Traceability", [])
    table_lines = [(line, raw) for line, raw in section if raw.strip().startswith("|")]
    if not table_lines:
        return rows, findings

    header_index: int | None = None
    header: list[str] = []
    for index, (line, raw) in enumerate(table_lines):
        cells = [cell.strip().lower() for cell in raw.strip().strip("|").split("|")]
        if cells == ["requirement", "acceptance", "verification", "status"]:
            header_index = index
            header = cells
            break
    if header_index is None:
        findings.append(
            Finding(
                "error",
                "TRACE001",
                "trace table must use Requirement | Acceptance | Verification | Status columns",
                document.section_lines.get("Verification and Traceability", 1),
            )
        )
        return rows, findings

    del header
    for line, raw in table_lines[header_index + 1 :]:
        cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if len(cells) != 4:
            findings.append(Finding("error", "TRACE002", "trace row must contain four columns", line))
            continue
        requirement, acceptance, verification, status = cells
        rows.append(
            TraceRow(requirement.upper(), acceptance.upper(), verification.upper(), status.lower(), line)
        )
    return rows, findings


def parse_reviews(document: Document) -> tuple[list[ReviewRecord], list[Finding]]:
    records: list[ReviewRecord] = []
    findings: list[Finding] = []
    for line, raw in document.sections.get("Verification and Traceability", []):
        if not re.search(r"\bREVIEW-\d+\b", raw, re.IGNORECASE):
            continue
        match = REVIEW_RE.match(raw)
        if not match:
            findings.append(
                Finding(
                    "error",
                    "REVIEW001",
                    "malformed review; expected '- REVIEW-001 | security | passed | reviewer: name | evidence: record'",
                    line,
                )
            )
            continue
        identifier, scope, status, reviewer, evidence = match.groups()
        records.append(
            ReviewRecord(
                identifier.upper(),
                scope.lower(),
                status.lower(),
                reviewer.strip(),
                evidence.strip(),
                line,
            )
        )
    return records, findings


def validate_document(document: Document, gate: str) -> tuple[list[Finding], dict[str, object]]:
    findings = list(document.parse_findings)
    metadata = document.metadata

    for key in METADATA_KEYS:
        if not metadata.get(key, "").strip():
            findings.append(Finding("error", "META005", f"missing required metadata: {key}"))
    for key in metadata:
        if key not in METADATA_KEYS and not key.startswith("x-"):
            findings.append(
                Finding("warning", "META006", f"unknown metadata key: {key}", document.metadata_lines.get(key, 1))
            )

    if metadata.get("status") and metadata["status"] not in VALID_STATUSES:
        findings.append(
            Finding("error", "META007", f"invalid status: {metadata['status']}", document.metadata_lines.get("status", 1))
        )
    profile = metadata.get("profile", "standard")
    if profile not in VALID_PROFILES:
        findings.append(
            Finding("error", "META008", f"invalid profile: {profile}", document.metadata_lines.get("profile", 1))
        )
        profile = "standard"
    if metadata.get("mode") and metadata["mode"] not in VALID_MODES:
        findings.append(
            Finding("error", "META009", f"invalid mode: {metadata['mode']}", document.metadata_lines.get("mode", 1))
        )
    if metadata.get("spec") and not re.fullmatch(r"SPEC-[A-Z0-9][A-Z0-9-]*", metadata["spec"]):
        findings.append(
            Finding("error", "META010", "spec ID must match SPEC-[A-Z0-9-]+", document.metadata_lines.get("spec", 1))
        )
    for key in ("created", "updated"):
        if metadata.get(key):
            try:
                dt.date.fromisoformat(metadata[key])
            except ValueError:
                findings.append(
                    Finding("error", "META011", f"{key} must be an ISO date (YYYY-MM-DD)", document.metadata_lines.get(key, 1))
                )

    if len(document.h1) != 1:
        findings.append(Finding("error", "STRUCT001", "document must contain exactly one H1 heading"))
    elif metadata.get("title") and document.h1[0][1] != metadata["title"]:
        findings.append(
            Finding("error", "STRUCT002", "H1 heading must equal frontmatter title", document.h1[0][0])
        )

    required_sections = PROFILE_SECTIONS[profile]
    for section in required_sections:
        if section not in document.sections:
            findings.append(Finding("error", "SECTION001", f"missing required section: {section}"))
        elif not section_text(document, section):
            findings.append(
                Finding("error", "SECTION002", f"required section is empty: {section}", document.section_lines[section])
            )

    for section in document.sections:
        if section not in CANONICAL_SECTIONS:
            findings.append(
                Finding("warning", "SECTION003", f"non-canonical section: {section}", document.section_lines[section])
            )

    findings.extend(_definition_duplicates(document))
    requirements, requirement_findings = parse_requirements(document)
    acceptance, acceptance_findings = parse_acceptance(document)
    trace, trace_findings = parse_trace(document)
    reviews, review_findings = parse_reviews(document)
    findings.extend(requirement_findings)
    findings.extend(acceptance_findings)
    findings.extend(trace_findings)
    findings.extend(review_findings)

    if not requirements:
        findings.append(
            Finding("error", "REQ002", "at least one normative requirement is required", document.section_lines.get("Requirements", 1))
        )
    if not acceptance:
        findings.append(
            Finding("error", "AC002", "at least one acceptance criterion is required", document.section_lines.get("Acceptance Criteria", 1))
        )

    requirement_by_id: dict[str, Requirement] = {}
    for item in requirements:
        requirement_by_id.setdefault(item.identifier, item)
    acceptance_by_id = {item.identifier: item for item in acceptance}
    acceptance_by_requirement: dict[str, list[Acceptance]] = {}
    for item in acceptance:
        acceptance_by_requirement.setdefault(item.requirement, []).append(item)
        if item.requirement not in requirement_by_id:
            findings.append(
                Finding("error", "AC003", f"{item.identifier} references unknown {item.requirement}", item.line)
            )
        if not _has_acceptance_structure(item.text):
            findings.append(
                Finding(
                    "warning",
                    "AC004",
                    f"{item.identifier} should express Given/When/Then behavior or a localized equivalent",
                    item.line,
                )
            )

    trace_by_requirement: dict[str, list[TraceRow]] = {}
    for row in trace:
        trace_by_requirement.setdefault(row.requirement, []).append(row)
        if row.requirement not in requirement_by_id:
            findings.append(Finding("error", "TRACE003", f"trace references unknown {row.requirement}", row.line))
        if row.acceptance not in acceptance_by_id:
            findings.append(Finding("error", "TRACE004", f"trace references unknown {row.acceptance}", row.line))
        elif acceptance_by_id[row.acceptance].requirement != row.requirement:
            findings.append(
                Finding("error", "TRACE005", f"{row.acceptance} belongs to {acceptance_by_id[row.acceptance].requirement}, not {row.requirement}", row.line)
            )
        if not re.fullmatch(r"TEST-\d{3,}", row.verification):
            findings.append(
                Finding("error", "TRACE006", f"verification must use a TEST-* identifier: {row.verification or '(empty)'}", row.line)
            )
        if row.status not in VALID_TRACE_STATUSES:
            findings.append(Finding("error", "TRACE007", f"invalid trace status: {row.status}", row.line))
        if row.status == "not-applicable" and not _decision_explains_requirement(document, row.requirement):
            findings.append(
                Finding(
                    "warning" if gate == "draft" else "error",
                    "TRACE008",
                    f"{row.requirement} marked not-applicable requires a DEC-* rationale",
                    row.line,
                )
            )

    for requirement in requirement_by_id.values():
        if AMBIGUOUS_RE.search(requirement.text):
            findings.append(
                Finding("warning", "REQ003", f"{requirement.identifier} contains an unbounded quality adjective", requirement.line)
            )
        if requirement.level not in VALID_LEVELS:
            findings.append(Finding("error", "REQ004", f"invalid normative level: {requirement.level}", requirement.line))
        if requirement.level in {"must", "must-not"}:
            if not acceptance_by_requirement.get(requirement.identifier):
                findings.append(
                    Finding("error", "COVERAGE001", f"{requirement.identifier} has no acceptance criterion", requirement.line)
                )
            if not trace_by_requirement.get(requirement.identifier):
                findings.append(
                    Finding("error", "COVERAGE002", f"{requirement.identifier} has no verification row", requirement.line)
                )

    body_start = 0
    if document.lines and document.lines[0].strip() == "---":
        closing = next((index for index in range(1, len(document.lines)) if document.lines[index].strip() == "---"), None)
        body_start = (closing + 1) if closing is not None else len(document.lines)
    lintable_lines = _markdown_prose(document.lines, body_start)
    for line_number, raw in enumerate(lintable_lines, 1):
        without_inline_code = re.sub(r"`[^`\n]*`", "", raw)
        match = PLACEHOLDER_RE.search(without_inline_code)
        if match:
            findings.append(Finding("warning" if gate == "draft" else "error", "CONTENT001", f"placeholder remains: {match.group(0)}", line_number, match.start() + 1))
        if re.search(r"\bN/A\b", without_inline_code, re.IGNORECASE) and not re.search(r"\bN/A\s+[—-]\s+\S", without_inline_code, re.IGNORECASE):
            findings.append(
                Finding("warning" if gate == "draft" else "error", "CONTENT002", "N/A requires a specific reason after an em dash", line_number)
            )

    for line, raw in document.sections.get("Open Questions", []):
        if not re.search(r"\bQ-\d+\b", raw, re.IGNORECASE):
            continue
        match = QUESTION_RE.match(raw)
        if not match:
            findings.append(
                Finding("error", "QUESTION001", "malformed question; expected '- Q-001 | blocking | text'", line)
            )
            continue
        identifier, status, _ = match.groups()
        status = status.lower()
        if status not in VALID_QUESTION_STATUSES:
            findings.append(Finding("error", "QUESTION002", f"invalid question status: {status}", line))
        if gate in {"ready", "verified"} and status == "blocking":
            findings.append(Finding("error", "QUESTION003", f"{identifier.upper()} remains blocking", line))

    if gate == "ready" and metadata.get("status") not in {"ready", "implemented", "verified"}:
        findings.append(Finding("error", "GATE001", "ready gate requires status ready, implemented, or verified", document.metadata_lines.get("status", 1)))
    if gate == "verified" and metadata.get("status") != "verified":
        findings.append(Finding("error", "GATE002", "verified gate requires status verified", document.metadata_lines.get("status", 1)))
    if gate in {"ready", "verified"} and _normalize_claim(metadata.get("owner", "")) == "unassigned":
        findings.append(
            Finding(
                "error",
                "OWNER001",
                "ready and verified specifications require an explicitly assigned owner",
                document.metadata_lines.get("owner", 1),
            )
        )
    if gate == "verified":
        for requirement in requirement_by_id.values():
            rows = trace_by_requirement.get(requirement.identifier, [])
            if requirement.level in {"must", "must-not"} and (
                not rows or any(row.status != "passed" for row in rows)
            ):
                findings.append(
                    Finding("error", "GATE003", f"{requirement.identifier} requires only passed verification rows", requirement.line)
                )
            elif requirement.level == "should" and (
                not rows or any(row.status not in {"passed", "not-applicable"} for row in rows)
            ):
                findings.append(
                    Finding(
                        "error",
                        "GATE005",
                        f"{requirement.identifier} requires passed evidence or an explained not-applicable disposition",
                        requirement.line,
                    )
                )
        for row in trace:
            if row.status in {"planned", "failed", "blocked"}:
                findings.append(
                    Finding("error", "GATE004", f"trace row is not closed: {row.status}", row.line)
                )

    if gate in {"ready", "verified"} and profile in {"standard", "critical"}:
        rollout_text = section_text(document, "Rollout and Rollback")
        for pattern, code, label in RISK_SECTION_CHECKS:
            if not re.search(pattern, rollout_text, re.IGNORECASE):
                findings.append(
                    Finding("warning", code, f"standard/critical spec should state a {label}", document.section_lines.get("Rollout and Rollback", 1))
                )

    if gate in {"ready", "verified"} and profile == "critical":
        for section, pattern, code, label in CRITICAL_SECTION_CHECKS:
            if not re.search(pattern, section_text(document, section), re.IGNORECASE):
                findings.append(
                    Finding("warning", code, f"critical spec should state {label}", document.section_lines.get(section, 1))
                )
        passed_reviews = [record for record in reviews if record.status == "passed"]
        valid_passed_reviews = [
            record
            for record in passed_reviews
            if _review_is_independent(record, metadata.get("owner", "")) and _review_has_evidence(record)
        ]
        for record in passed_reviews:
            if not _review_is_independent(record, metadata.get("owner", "")):
                findings.append(
                    Finding(
                        "error",
                        "REVIEW003",
                        f"{record.identifier} reviewer must differ from the spec owner and cannot be self-declared",
                        record.line,
                    )
                )
            if not _review_has_evidence(record):
                findings.append(
                    Finding(
                        "error",
                        "REVIEW004",
                        f"{record.identifier} passed review requires concrete evidence",
                        record.line,
                    )
                )
        if not valid_passed_reviews:
            findings.append(
                Finding(
                    "error",
                    "CRIT005",
                    "critical readiness requires a structured passed independent review record",
                    document.section_lines.get("Verification and Traceability", 1),
                )
            )
        for record in reviews:
            if record.status in {"failed", "blocked"}:
                findings.append(
                    Finding("error", "REVIEW002", f"{record.identifier} remains {record.status}", record.line)
                )

    findings = sorted(
        set(findings),
        key=lambda item: (item.line, item.column, SEVERITY_ORDER[item.severity], item.code, item.message),
    )
    summary: dict[str, object] = {
        "profile": profile,
        "gate": gate,
        "requirements": len(requirement_by_id),
        "acceptance_criteria": len(acceptance),
        "trace_rows": len(trace),
        "reviews": len(reviews),
        "errors": sum(item.severity == "error" for item in findings),
        "warnings": sum(item.severity == "warning" for item in findings),
        "notes": sum(item.severity == "note" for item in findings),
    }
    return findings, summary


def _finding_payload(document: Document, finding: Finding) -> dict[str, object]:
    return {"path": document.display_path, **asdict(finding)}


def render_text(document: Document, findings: Sequence[Finding], summary: dict[str, object], passed: bool) -> str:
    lines = []
    for finding in findings:
        lines.append(
            f"{document.display_path}:{finding.line}:{finding.column}: {finding.severity} {finding.code}: {finding.message}"
        )
    verdict = "PASS" if passed else "FAIL"
    lines.append(
        f"{verdict} {document.display_path} ({summary['gate']}/{summary['profile']}): "
        f"{summary['errors']} error(s), {summary['warnings']} warning(s), "
        f"{summary['requirements']} requirement(s), {summary['trace_rows']} trace row(s)"
    )
    return "\n".join(lines)


def render_json(document: Document, findings: Sequence[Finding], summary: dict[str, object], passed: bool) -> str:
    return json.dumps(
        {
            "version": "1",
            "path": document.display_path,
            "passed": passed,
            "summary": summary,
            "findings": [_finding_payload(document, finding) for finding in findings],
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


def render_sarif(document: Document, findings: Sequence[Finding]) -> str:
    rules: dict[str, dict[str, object]] = {}
    results = []
    for finding in findings:
        rules.setdefault(
            finding.code,
            {"id": finding.code, "shortDescription": {"text": finding.message}},
        )
        results.append(
            {
                "ruleId": finding.code,
                "level": {"error": "error", "warning": "warning", "note": "note"}[finding.severity],
                "message": {"text": finding.message},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": document.display_path},
                            "region": {
                                "startLine": finding.line,
                                "startColumn": finding.column,
                            },
                        }
                    }
                ],
            }
        )
    payload = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Evidrail",
                        "informationUri": "https://github.com/dimidotdev/evidrail",
                        "rules": [rules[key] for key in sorted(rules)],
                    }
                },
                "results": results,
            }
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def _slug_identifier(path: Path) -> str:
    slug = re.sub(r"[^A-Z0-9]+", "-", path.stem.upper()).strip("-") or "CHANGE"
    if slug.startswith("SPEC-"):
        slug = slug.removeprefix("SPEC-") or "CHANGE"
    return f"SPEC-{slug}-0001"


def command_init(args: argparse.Namespace) -> int:
    target = Path(args.path)
    if target.is_symlink():
        print(f"evidrail: refusing to overwrite a symbolic link: {target}", file=sys.stderr)
        return EXIT_IO
    if target.exists() and not args.force:
        print(f"evidrail: refusing to overwrite existing file: {target}", file=sys.stderr)
        return EXIT_IO
    template_name = "spec-template-light.md" if args.profile == "light" else "spec-template.md"
    template_path = Path(__file__).resolve().parent.parent / "assets" / template_name
    temporary_path: Path | None = None
    try:
        template = template_path.read_text(encoding="utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        today = dt.date.today().isoformat()
        title = args.title.strip()
        spec_id = args.spec_id or _slug_identifier(target)
        owner = (args.owner or "unassigned").strip()
        if not title:
            print("evidrail: title must not be empty", file=sys.stderr)
            return EXIT_USAGE
        if not owner:
            print("evidrail: owner must not be empty", file=sys.stderr)
            return EXIT_USAGE
        if not re.fullmatch(r"SPEC-[A-Z0-9][A-Z0-9-]*", spec_id):
            print("evidrail: spec ID must match SPEC-[A-Z0-9-]+", file=sys.stderr)
            return EXIT_USAGE
        replacements = {
            "spec: SPEC-0001": f"spec: {spec_id}",
            "title: TODO": f"title: {json.dumps(title, ensure_ascii=False)}",
            "profile: standard": f"profile: {args.profile}",
            "mode: deliver": f"mode: {args.mode}",
            "owner: TODO": f"owner: {json.dumps(owner, ensure_ascii=False)}",
            "created: YYYY-MM-DD": f"created: {today}",
            "updated: YYYY-MM-DD": f"updated: {today}",
            "# TODO": f"# {title}",
        }
        for source, destination in replacements.items():
            template = template.replace(source, destination, 1)
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=target.parent,
            prefix=".evidrail-",
            suffix=".tmp",
            delete=False,
            newline="\n",
        ) as temporary:
            temporary.write(template)
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, target)
        temporary_path = None
    except (OSError, UnicodeError) as exc:
        print(f"evidrail: cannot initialize {target}: {exc}", file=sys.stderr)
        return EXIT_IO
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    print(_display_path(target))
    return EXIT_OK


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name


def command_check(args: argparse.Namespace) -> int:
    path = Path(args.path)
    try:
        document = parse_document(path, _display_path(path))
    except IOError as exc:
        print(f"evidrail: {exc}", file=sys.stderr)
        return EXIT_IO
    findings, summary = validate_document(document, args.gate)
    fail_on_warning = args.strict or (document.metadata.get("profile") == "critical" and args.gate != "draft")
    passed = not any(item.severity == "error" for item in findings) and not (
        fail_on_warning and any(item.severity == "warning" for item in findings)
    )
    if args.format == "json":
        output = render_json(document, findings, summary, passed)
    elif args.format == "sarif":
        output = render_sarif(document, findings)
    else:
        output = render_text(document, findings, summary, passed)
    print(output)
    return EXIT_OK if passed else EXIT_FINDINGS


def _trace_payload(document: Document) -> tuple[dict[str, object], bool]:
    requirements, requirement_findings = parse_requirements(document)
    acceptance, acceptance_findings = parse_acceptance(document)
    rows, trace_findings = parse_trace(document)
    acceptance_by_requirement: dict[str, list[str]] = {}
    for item in acceptance:
        acceptance_by_requirement.setdefault(item.requirement, []).append(item.identifier)
    rows_by_requirement: dict[str, list[TraceRow]] = {}
    for row in rows:
        rows_by_requirement.setdefault(row.requirement, []).append(row)

    unique_requirements: dict[str, Requirement] = {}
    for requirement in requirements:
        unique_requirements.setdefault(requirement.identifier, requirement)
    matrix = []
    unresolved = False
    for requirement in unique_requirements.values():
        requirement_rows = rows_by_requirement.get(requirement.identifier, [])
        covered_acceptance = sorted({row.acceptance for row in requirement_rows})
        expected_acceptance = sorted(acceptance_by_requirement.get(requirement.identifier, []))
        missing_acceptance = sorted(set(expected_acceptance) - set(covered_acceptance))
        gated_levels = {"must", "must-not"}
        if document.metadata.get("status") == "verified":
            gated_levels.add("should")
        if requirement.level in gated_levels and (not requirement_rows or missing_acceptance):
            unresolved = True
        matrix.append(
            {
                "requirement": requirement.identifier,
                "level": requirement.level,
                "acceptance": expected_acceptance,
                "verification": sorted({row.verification for row in requirement_rows}),
                "statuses": sorted({row.status for row in requirement_rows}),
                "missing_acceptance": missing_acceptance,
            }
        )
    validation_gate = "verified" if document.metadata.get("status") == "verified" else "draft"
    validation_findings, _ = validate_document(document, validation_gate)
    structural_errors = [item for item in validation_findings if item.severity == "error"]
    if requirement_findings or acceptance_findings or trace_findings or structural_errors:
        unresolved = True
    return {
        "version": "1",
        "path": document.display_path,
        "complete": not unresolved,
        "matrix": matrix,
        "findings": [asdict(item) for item in structural_errors],
    }, not unresolved


def command_trace(args: argparse.Namespace) -> int:
    path = Path(args.path)
    try:
        document = parse_document(path, _display_path(path))
    except IOError as exc:
        print(f"evidrail: {exc}", file=sys.stderr)
        return EXIT_IO
    payload, complete = _trace_payload(document)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"Traceability: {payload['path']}")
        for finding in payload["findings"]:
            print(f"- issue {finding['code']} at line {finding['line']}: {finding['message']}")
        for item in payload["matrix"]:
            acceptance = ", ".join(item["acceptance"]) or "—"
            verification = ", ".join(item["verification"]) or "—"
            statuses = ", ".join(item["statuses"]) or "uncovered"
            missing = ", ".join(item["missing_acceptance"])
            suffix = f"; missing: {missing}" if missing else ""
            print(
                f"- {item['requirement']} ({item['level']}): AC [{acceptance}] -> TEST [{verification}] -> {statuses}{suffix}"
            )
        print("PASS traceability complete" if complete else "FAIL traceability gaps remain")
    return EXIT_OK if complete else EXIT_FINDINGS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evidrail",
        description="Initialize, validate, and trace evidence-backed software specifications.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create a spec from the canonical template")
    init_parser.add_argument("path")
    init_parser.add_argument("--title", required=True)
    init_parser.add_argument("--profile", choices=sorted(VALID_PROFILES), default="standard")
    init_parser.add_argument("--mode", choices=sorted(VALID_MODES), default="deliver")
    init_parser.add_argument("--spec-id")
    init_parser.add_argument("--owner")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=command_init)

    check_parser = subparsers.add_parser("check", help="validate structure, readiness, and evidence")
    check_parser.add_argument("path")
    check_parser.add_argument("--gate", choices=("draft", "ready", "verified"), default="ready")
    check_parser.add_argument("--format", choices=("text", "json", "sarif"), default="text")
    check_parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    check_parser.set_defaults(func=command_check)

    trace_parser = subparsers.add_parser("trace", help="show requirement-to-test coverage")
    trace_parser.add_argument("path")
    trace_parser.add_argument("--format", choices=("text", "json"), default="text")
    trace_parser.set_defaults(func=command_trace)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
