---
spec: SPEC-LIGHT-0001
title: "Focused local fix"
status: ready
profile: light
mode: deliver
owner: tests
created: 2026-07-29
updated: 2026-07-29
---

# Focused local fix

## Context and Evidence

- EVD-001 | source: regression test | The existing formatter emits a trailing blank line.

## Problem

The extra blank line breaks exact-output consumers.

## Outcomes

- Restore the documented one-line output.

## Non-goals

- Change formatting for multi-line input.

## Current Behavior

One-line input produces two output lines.

## Proposed Behavior

One-line input produces exactly one output line.

## Requirements

- REQ-001 | must | When one-line input is formatted, the system shall emit exactly one output line.

## Acceptance Criteria

- AC-001 | REQ-001 | Given one-line input, when formatting completes, then output contains no trailing blank line.

## Security and Privacy

- N/A — the local pure-text formatter changes no authority, trust boundary, stored data, logging, or external input path.

## Verification and Traceability

| Requirement | Acceptance | Verification | Status |
| --- | --- | --- | --- |
| REQ-001 | AC-001 | TEST-001 | planned |

## Decisions

- DEC-001 | Remove only the redundant terminal newline. | rationale: preserve every other documented formatting invariant. | affects: REQ-001

## Open Questions

- None — the regression and expected output are directly observed.
