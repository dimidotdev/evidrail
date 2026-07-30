---
spec: SPEC-INVALID-0001
title: "Invalid fixture"
status: ready
profile: light
mode: deliver
owner: tests
created: 2026-07-29
updated: 2026-07-29
---

# Invalid fixture

## Context and Evidence

- EVD-001 | source: TODO | This fixture intentionally fails.

## Problem

The contract is incomplete.

## Outcomes

- Expose deterministic findings.

## Non-goals

- Repair the fixture automatically.

## Current Behavior

Coverage is missing.

## Proposed Behavior

The validator reports each defect.

## Requirements

- REQ-001 | must | The system shall be robust.
- REQ-001 | must | The system shall report duplicate definitions.

## Acceptance Criteria

- AC-001 | REQ-999 | Given invalid input, when validation runs, then it fails.

## Security and Privacy

- N/A

## Verification and Traceability

| Requirement | Acceptance | Verification | Status |
| --- | --- | --- | --- |
| REQ-999 | AC-999 | TEST-X | planned |

## Open Questions

- Q-001 | blocking | Which behavior is expected?
