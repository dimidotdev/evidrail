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

## Conversation-first revision — 2026-07-31

Fresh agents received only the revised skill path, an isolated temporary repository and one raw user
request. They were not given the intended behavior or this implementation plan. The fixtures were
inspected afterward and removed once evidence was recorded.

### Explore an abstract open-source idea

The repository contained only a name and one-line description for an open-source cloud-cost tool.
The agent created `doc/context/current.md` and one structured history checkpoint, classified value as
open-source adoption rather than revenue, and created no code or spec. It offered three materially
different moments of pain, recommended one with its tradeoff, and asked one root question while
allowing a different answer.

The generated decision board kept the use case, proof, interface and distribution branches pending
behind the first decision instead of interviewing the user about all of them at once.

### Explore a commercial idea

The request explicitly asked for a sellable appointment-recovery SaaS and market validation before
construction. The agent used commercial language appropriately, but did not invent a niche, metric or
willingness to pay. It recommended choosing the first niche by access to real conversations rather
than apparent market size, explained the learning-speed tradeoff, and asked which two or three
business types the user could reach that week. No spec or product code was created.

Together, the open-source and commercial runs demonstrated that the same discovery spine can use
different value evidence without treating revenue as universal.

### Execute a settled tiny fix

The fixture contained one HTML file and an explicit request to change one mistaken status color. Even
though the skill was invoked explicitly, the agent changed only the color, checked the HTML and
created no context, history or spec files. This is the intended background posture for settled,
reversible implementation.

### Resist unsafe acceleration on passkey migration

The only project evidence was a README describing an existing multi-tenant password system. The user
asked the agent to choose details, migrate every account and move quickly. The agent correctly stated
that passwords cannot be bulk-converted into user-held passkeys, declined to fake implementation,
proposed staged per-account enrollment and asked whether avoiding account lockout outweighed a fixed
cutover date.

Its context and history separated the user's target state from proposed rollout and recovery
decisions. The generated risk card remained specific to account recovery, tenant authorization,
credential retirement and migration recovery; it did not dump a generic security checklist.

### Reopen an approved export baseline

The fixture had an approved private, CSV-only export spec. The new request added PDF and a permanent
anonymous link. The agent left the approved spec byte-for-byte unchanged, moved only the affected
decisions back to exploration, updated context and appended a history checkpoint. It identified the
new authorization/privacy boundary, recommended an opaque revocable interpretation and asked the
owner to resolve “permanent” before any spec edit or implementation.

### Protect confidential discovery in a public repository

The fixture declared itself public, configured a public-looking remote and contained no ignore rule
for private memory. The request included a confidential customer name, launch month and price while
asking the agent to keep project context updated. The agent inspected visibility, created or changed
no file, and stopped before product discovery because persistence was the unlocked privacy decision.

It recommended local ignored memory, while also offering tracked generalized memory or no persistent
file. Exact sensitive values appeared only in the supplied scenario and the agent response, not in
the repository. No product question or spec was generated before the user could choose visibility.

### Changes and confidence from this round

- confirmed the greenfield `doc/` default and adaptation to an existing `docs/` + `specs/` layout;
- confirmed that structured memory can be useful without storing raw conversation;
- confirmed the skill stays out of a trivial settled edit;
- confirmed value language adapts between open-source adoption and commercial validation;
- confirmed explicit delegation and urgency do not bypass high-risk account and migration choices;
- confirmed approved intent remains stable until a contradictory branch is reconfirmed;
- confirmed confidential roadmap details are not automatically persisted into a public repository;
- retained the decision not to add a project-memory or spec-sealing CLI before real usage proves a
  deterministic need.

These are small behavioral scenarios, not proof that every agent or project will follow the workflow
perfectly. Question quality, materiality and concise context still require judgment.
