# Verification and Delivery

## Match evidence to the claim

| Claim | Preferred evidence |
| --- | --- |
| pure logic | unit/property test |
| module collaboration | integration/contract test |
| user interaction | browser or device-level test |
| database state | migration rehearsal and database assertion |
| authorization | negative integration tests at enforcement boundary |
| performance | measured budget under representative conditions |
| deployment/config | dry run plus production smoke/health check |
| accessibility | semantic review, automated scan, keyboard/reflow check |
| recovery | induced failure plus rollback/forward-recovery evidence |

Avoid proving a high-level claim only with a low-level test.

## Change-type minimums

- Bugfix: capture reproduction, observed versus expected behavior, root cause, and a regression check; show failure before the fix when feasible.
- Feature: verify the user outcome, states and errors, contract changes, compatibility, and documentation.
- Refactor: name preserved invariants, establish characterization evidence, and prove before/after parity.
- Hardening: define the threat or failure model, abuse cases, controls, negative tests, operational signals, and recovery.

## Traceability lifecycle

1. Before implementation, every `must`/`must-not` requirement has an `AC-*` and planned `TEST-*`.
2. During implementation, update the test description or trace row when the boundary changes.
3. After checks run, change `planned` to `passed`, `failed`, or `blocked` with concise evidence.
4. Never erase a failed result to make the table green; record the resolution or superseding decision.

## Observability

Derive telemetry from failure modes and operator decisions. Define:

- event or metric name;
- boundary and dimensions with bounded cardinality;
- success/failure interpretation;
- alert or investigation threshold where justified;
- sensitive-data exclusions;
- owner and response action.

Do not add logs that nobody can use or alerts without an action.

## Rollout and rollback

For standard/critical changes, specify:

- sequencing and compatibility window;
- feature flag, cohort, canary, or staged deployment where useful;
- pre-deploy checks and backups;
- health signals and stop conditions;
- rollback command or forward-fix procedure;
- state reconciliation after partial success;
- communication or audit requirements.

Prefer expand/migrate/contract for incompatible data changes. A rollback that cannot read newly written state is not a rollback.

## Completion report

Lead with the outcome. Include:

- requirements delivered and intentionally deferred;
- verification evidence and environment;
- assumptions validated or disproven;
- security/design decisions that materially shaped the result;
- residual risks;
- rollout/rollback state;
- links to spec, code, CI, and production when applicable.
