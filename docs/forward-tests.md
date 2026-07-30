# Forward-test notes

Evidrail was tested by fresh agents that received only the skill path, one bounded fixture, and a user request. They were not given intended answers or implementation plans. Product code remained read-only. This is a behavior test of the skill, not a benchmark claim.

## Scenarios

### Audit an invalid specification

The agent selected `audit/light`, ran both commands, separated specification defects from verification gaps, and explicitly refused to invent implementation defects without code or runtime evidence. The current fixture remains in `tests/fixtures/invalid-spec.md` and is expected to fail deterministically.

### Specify a local route-layout bug

The fixture contains one HTML page, one stylesheet, and one navigation script. Loading copy appears briefly in normal flow and shifts the content.

The first agent selected `standard` because the change affected visible and accessible behavior. Its valid artifact was 16 KB, which exposed ambiguous profile guidance and too much ceremony for a reversible local fix. It also discovered that the trace grammar accepted one acceptance and one test identifier per row while the reference did not say so.

After revising classification and documenting the table grammar, a fresh agent correctly selected `light`. Its 11 KB artifact revealed that `init` still emitted the full canonical template and derived a redundant identifier from filenames beginning with `spec-`.

After adding a light micro-template and identifier normalization, a third fresh agent produced a 90-line ready artifact with five requirements and complete traceability. Its remaining friction was the lack of a dedicated compact decision section; the light contract now includes one.

### Specify a sensitive tenant export

The fixture is a multi-tenant route that returns customer names, email addresses, and phone numbers without an evidenced role check. The request asks for an asynchronous CSV export.

Both fresh agents selected `critical` and covered authorization, tenant isolation, requester ownership, CSV formula injection, private storage, bounded generation, retries, retention, auditing, telemetry, staged rollout, and forward recovery. The first run exposed a validator weakness: prose containing “independent review” could satisfy the mechanical prompt even when review was only planned.

Evidrail now requires a structured `REVIEW-*` record with `passed` state, reviewer identity, and evidence before a critical spec can be ready. The second run kept review records planned and the artifact in draft. Its ready gate failed on draft status, missing passed review, and three blocking questions; traceability itself passed. The agent also stated that the validator cannot prove reviewer independence or evidence authenticity.

The critical artifact was approximately 46 KB. That size is not a target. Critical work requires full risk and recovery reasoning, but teams should remove repetition or split the artifact when navigation suffers.

## Changes caused by testing

- clarified that risk and diff size are independent;
- made reversible UI bugfixes eligible for `light` without skipping accessibility;
- added a dedicated light micro-template;
- added compact decisions to the light contract;
- documented one REQ, AC, and TEST identifier per trace row;
- normalized generated IDs for paths beginning with `spec-`;
- replaced keyword-based critical review detection with structured evidence;
- de-duplicated coverage diagnostics after duplicate requirement definitions;
- taught trace mode to fail on structural and referential errors.

## Remaining limits

- A passing validator proves structural invariants, not product value or system security.
- Structured review evidence can still be dishonest; human governance remains necessary.
- The skill cannot discover facts unavailable in the repository or authorized environment.
- Proportionality still requires judgment, especially near the light/standard boundary.
- Forward-test fixtures are intentionally small and do not establish performance at repository scale.
