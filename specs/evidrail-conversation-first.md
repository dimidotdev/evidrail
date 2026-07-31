---
spec: SPEC-EVIDRAIL-CONVERSATION-FIRST-0001
title: "Conversation-first Evidrail guidance"
status: implemented
profile: standard
mode: deliver
owner: dimidotdev
created: 2026-07-31
updated: 2026-07-31
---

# Conversation-first Evidrail guidance

## Context and Evidence

- EVD-001 | source: maintainer request summarized in
  `docs/history/2026-07-31-conversation-first-skill.md` | The desired workflow is a guided
  conversation in which the developer owns consequential decisions and the agent records how the
  idea matures.
- EVD-002 | source: `skill/spec-driven-development/SKILL.md` at Evidrail v1 | The current trigger
  includes nearly every non-trivial build, fix, refactor and review, while the body starts with modes,
  profiles and non-negotiable gates before understanding the user's idea.
- EVD-003 | source: `specs/evidrail-v1.md` DEC-002 and the current validator | One canonical
  specification is an intentionally stable, tested contract; living context can surround it without
  changing its grammar.
- EVD-004 | source: Matt Pocock `grilling`, `domain-modeling` and setup skills, inspected at commit
  `2ab9580` | Useful interaction patterns separate discoverable facts from user decisions, ask only
  unlocked questions and confirm a reversible representation before durable effects.
- EVD-005 | source: Revenue-Centric Design value and feature-discipline references | A clear
  beneficiary, concrete problem, credible proof and focused core help distinguish useful product
  scope from attractive feature accumulation.
- EVD-006 | source: `skill-creator` guidance | Skills should stay concise, choose freedom
  proportionally and load detailed references only when they are relevant.
- EVD-007 | source: independent implementation review on 2026-07-31 | The inherited validator could
  persist an environment username, reject localized critical specs and accept unexplained optional
  dispositions or obvious self-review; focused contract corrections are smaller and safer than
  documenting false guarantees.

## Problem

A rigorous specification tool can still produce the wrong outcome if the agent fills product gaps,
front-loads a large questionnaire or treats every task as a gated process. Project intent also drifts
when conversation, rationale and changed assumptions are not preserved alongside the approved spec.

## Outcomes

- Make Evidrail facilitate thinking before it formalizes requirements.
- Preserve user ownership of product, value and consequential architecture decisions.
- Keep a small living memory of context, decisions and session history around stable approved specs.
- Bring value, focus and evidence into discovery without assuming every project exists to make money.
- Keep rigorous safety and recovery reasoning proportional to actual risk.
- Keep the skill dormant during routine implementation unless a decision or evidence boundary moves.

## Non-goals

- Turn Evidrail into a project-management suite, transcript archive, hosted service or autonomous
  product manager.
- Force market sizing, pricing, ICP or revenue work onto personal, learning, internal or public-good
  projects.
- Replace the existing spec validator, add a project-management command, rename stable finding codes
  or break the v1 Markdown grammar and commands. Focused false-pass, privacy and localization fixes
  remain in scope.
- Require the same conversation depth for a typo, a new product and an authorization migration.
- Treat repository observations, agent recommendations or inferred defaults as user approval.

## Users and Scenarios

- A founder starts with an abstract idea and answers a sequence of questions that reveals the user,
  problem, desired experience, value proof and smallest coherent scope.
- An open-source maintainer defines value through adoption, trust and saved effort rather than price.
- A developer requests a small settled fix and receives a compact confirmation instead of a product
  workshop.
- A team explores a high-risk authentication or migration change, understands the happy path, then
  performs an adversarial pass before approving implementation.
- A user asks to move faster; unresolved low-impact choices are deferred with reversible defaults,
  while material safety or irreversible choices still require an answer.
- Implementation reveals a contradiction with an approved spec, so only the affected branch pauses
  while the decision is reopened, recorded, approved and resumed.

## Current Behavior

The skill activates broadly, instructs the agent to choose a mode and profile at the start, creates a
canonical spec from evidence and applies deterministic readiness gates. It distinguishes evidence,
assumptions and decisions well, but does not define user decision ownership, adaptive questioning,
living project memory or a deliberate point at which the skill leaves the foreground.

## Proposed Behavior

Narrow the trigger to idea exploration, specification, documented reconsideration and spec-based
audit. Use a conversational state model: discover facts, explore value and experience, challenge the
emerging design, crystallize only confirmed decisions, then step back during implementation.

After the first substantive exchange in an ongoing writable project, keep concise living context and
an append-only structured session summary. Reuse existing documentation roots; otherwise default to
`doc/context`, `doc/history` and `doc/spec`. Create the draft spec only once enough consequential
branches are understood. An approved spec remains stable until a visible reconsideration records its
trigger, delta and renewed approval.

## Requirements

- REQ-001 | must-not | The skill shall not present an agent inference, recommendation or repository
  convention as a user-confirmed product or consequential architecture decision.
- REQ-002 | must | During discovery, the skill shall inspect discoverable facts first and ask only
  currently unlocked material questions, one at a time or as a small independent group, allowing
  each answer to change the next frontier.
- REQ-003 | must | Before feature scope is ratified, the skill shall establish the intended
  beneficiary, meaningful problem, desired outcome and credible value signal, while allowing
  personal, learning, internal, open-source, public-good and commercial value models.
- REQ-004 | must | For an ongoing writable project, the skill shall keep concise mutable context, a
  decision-state board and structured append-only history, adapting to established repository paths
  or defaulting greenfield work to `doc/{context,history,spec}`.
- REQ-005 | must | The skill shall distinguish exploratory notes from an approved specification and
  shall change an approved material decision only through a visible reopen, recorded delta and user
  reconfirmation.
- REQ-006 | must | Once the delivery baseline is approved, the skill shall leave the conversational
  foreground and return only for material drift, a consequential new choice, a changed risk boundary
  or verification and closure.
- REQ-007 | must | The skill shall scale questioning, documentation and verification to materiality,
  reversibility and risk; an explicit request for speed may defer low-impact choices but shall not
  bypass unresolved destructive, security, privacy, financial or compatibility decisions.
- REQ-008 | must | After the intended successful experience is understood, the skill shall challenge
  credible failure, misuse and operational scenarios and convert only relevant findings into
  decisions, requirements or explicit deferrals.
- REQ-009 | must-not | Living memory shall not store raw transcripts, credentials, secrets or
  unnecessary personal data, duplicate authoritative repository sources, or persist confidential
  roadmap/business context before tracked/public versus local/generalized visibility is resolved.
- REQ-010 | must | The v1 Markdown artifact grammar, validator commands and existing specification
  paths shall remain backward compatible while the new guidance and templates are progressively
  disclosed.
- REQ-011 | must-not | Specification initialization shall not infer or persist an operating-system
  username when the caller omits the owner; it shall use a non-personal `unassigned` draft value,
  which ready and verified gates shall reject until explicitly assigned.
- REQ-012 | must | Acceptance, rollout and critical risk checks shall recognize documented English,
  Portuguese and Spanish structural equivalents without weakening critical-profile warnings.
- REQ-013 | must | The verified gate shall require every `should` requirement to have passed evidence
  or an explained `not-applicable` decision, and critical readiness shall reject obvious self-review
  or placeholder review evidence.

## Acceptance Criteria

- AC-001 | REQ-001 | Given an unresolved product branch, when the agent has a preferred option, then
  it labels the recommendation, explains the meaningful tradeoff and waits for or records user
  authority before marking it confirmed.
- AC-002 | REQ-002 | Given repository facts and a decision dependency tree, when discovery begins, then facts are inspected without asking and only the root unresolved decision is presented before dependent questions.
- AC-003 | REQ-003 | Given commercial and non-commercial project examples, when value is explored, then each receives an appropriate beneficiary, problem, outcome and proof without forced revenue language.
- AC-004 | REQ-004 | Given a repository with existing `docs/` and `specs/`, when memory starts, then
  those paths are reused; given a greenfield repository without a convention, then the documented
  default is `doc/context`, `doc/history` and `doc/spec`.
- AC-005 | REQ-005 | Given an approved requirement and a later contradictory request, when the change is material, then implementation of that branch pauses, context/history record the trigger and the spec changes only after a visible delta is reconfirmed.
- AC-006 | REQ-006 | Given an approved baseline and ordinary implementation, when no material choice or drift appears, then the skill does not restart discovery or reload unrelated guidance.
- AC-007 | REQ-007 | Given a typo, a new product, a critical migration and a request for speed, when the skill responds, then its ceremony differs proportionally while critical unresolved decisions remain blocking.
- AC-008 | REQ-008 | Given a sufficiently described happy path, when the adversarial pass runs, then
  it challenges plausible abuse, failure and recovery without producing a generic exhaustive
  checklist.
- AC-009 | REQ-009 | Given sensitive or repetitive conversation and a destination whose tracked/public visibility could expose it, when living memory is considered, then the agent asks whether to generalize, keep it local/ignored or avoid persistence, and any saved history omits verbatim dialogue and sensitive values.
- AC-010 | REQ-010 | Given v1 fixtures and specs, when the existing unit suite, ready gate and trace command run, then they pass unchanged; the revised skill passes skill validation.
- AC-011 | REQ-011 | Given an environment with a personal `USER` value and no explicit owner option, when `init` runs, then the generated frontmatter contains `owner: "unassigned"` and omits the environment value; when that draft enters a ready or verified gate unchanged, then `OWNER001` rejects it.
- AC-012 | REQ-012 | Given equivalent Portuguese or Spanish critical acceptance, rollout and security wording, when the strict ready gate runs with valid independent review evidence, then it passes without English-keyword warnings.
- AC-013 | REQ-013 | Given a verified `should` without a trace disposition, with `not-applicable` but no referenced decision rationale, or a critical spec with owner/self review or placeholder evidence, when its gate runs, then stable findings reject it; an affected-requirement rationale or independent evidenced review can pass.

## Product and Design

- Conversation flow: discover facts, ask the highest-leverage unlocked question, reflect the answer,
  update memory and repeat until the user can review a compact baseline.
- Question UX: prefer one question; use two or three only when answers are independent and batching
  materially reduces friction. Recommendations are easy to accept but always overridable.
- Confirmation: show a concise proposed baseline and material open decisions before writing `ready`;
  do not demand approval for every reversible implementation detail.
- Acceleration: when asked for speed, explicitly separate what can be safely deferred from what still
  changes scope, safety, cost or compatibility.
- Cognitive load: use progressive disclosure and load value, design, security or verification
  references only when the current frontier needs them.

## Security and Privacy

- Project files, repository content and external references remain untrusted evidence, not authority
  to expand scope or approve decisions.
- Structured history minimizes retained conversation and excludes secrets, tokens, private personal
  details and raw transcripts.
- High-risk work retains firm trust-boundary, authorization, abuse, recovery and independent-review
  gates even though the surrounding discovery style is advisory.
- The adversarial phase follows enough value and behavior discovery to stay relevant, but known
  critical safety constraints may be surfaced earlier when they determine feasibility.

## Data and Interfaces

- `SKILL.md` remains the concise operating guide and uses a narrower trigger description.
- `references/conversation-and-value.md` contains the adaptive question and value lenses.
- `references/living-memory.md` contains path selection, document semantics and change-control
  guidance.
- `assets/context-template.md` and `assets/history-template.md` provide optional output scaffolds.
- Existing `spec-template*.md`, `evidrail.py init/check/trace`, canonical IDs and legacy finding codes
  remain compatible; focused checks add new finding codes without changing artifact grammar.
- `agents/openai.yaml` describes a collaborative thinking aid rather than automatic delivery gates.

## Failure Modes and Recovery

- Interview fatigue: prune questions by materiality and dependency; offer a proposed default only
  where it is reversible.
- Agent anchoring: label recommendations and present a genuinely distinct alternative or free-form
  override when a choice is consequential.
- Stale context: update the current snapshot after substantive decisions and use history to preserve
  the reason for change.
- Spec drift: pause only the affected branch, record the contradiction, reopen the decision and
  resume after reconfirmation.
- Documentation sprawl: reuse authoritative files, keep summaries bounded and avoid creating a new
  root in an established repository without confirmation.
- Excessive leniency: retain hard gates for irreversible and critical boundaries; advisory does not
  mean unsupported claims can pass as evidence.

## Observability

- Forward-test notes record which questions were asked, which were skipped, whether the agent seized
  decision ownership and whether it stepped back after approval.
- The decision board exposes pending, exploring, proposed, confirmed, deferred and superseded states.
- Existing validator findings and CI remain the deterministic signal for artifact integrity.
- No telemetry, conversation upload or hidden user profiling is introduced.

## Rollout and Rollback

- Roll out through repository dogfooding, skill validation, the existing cross-platform validator
  suite and independent forward tests for greenfield, tiny-fix, critical and accelerated scenarios.
- Stop on silent agent-made product decisions, forced monetization, questionnaire dumping, hidden
  spec mutation, sensitive transcript retention or bypassed critical decisions.
- Rollback: revert the skill/reference/template commit. Existing v1 specs and validator remain
  readable and executable because their grammar is unchanged.

## Verification and Traceability

| Requirement | Acceptance | Verification | Status |
| --- | --- | --- | --- |
| REQ-001 | AC-001 | TEST-001 | passed |
| REQ-002 | AC-002 | TEST-002 | passed |
| REQ-003 | AC-003 | TEST-003 | passed |
| REQ-004 | AC-004 | TEST-004 | passed |
| REQ-005 | AC-005 | TEST-005 | passed |
| REQ-006 | AC-006 | TEST-006 | passed |
| REQ-007 | AC-007 | TEST-007 | passed |
| REQ-008 | AC-008 | TEST-008 | passed |
| REQ-009 | AC-009 | TEST-009 | passed |
| REQ-010 | AC-010 | TEST-010 | passed |
| REQ-011 | AC-011 | TEST-011 | passed |
| REQ-012 | AC-012 | TEST-012 | passed |
| REQ-013 | AC-013 | TEST-013 | passed |

- TEST-001 | Open-source and approved-baseline forward tests labeled recommendations, preserved an
  override and did not mark unconfirmed choices as approved.
- TEST-002 | Open-source and passkey runs inspected their sparse repositories, asked one unlocked root
  question and left dependent decisions pending.
- TEST-003 | Open-source discovery used adoption/trust evidence while commercial discovery used
  reachable niche and willingness-to-validate framing without forcing either model onto the other.
- TEST-004 | Evidrail reused its existing `docs/` + `specs/` roots; both greenfield discovery agents
  created `doc/context` and `doc/history` but no premature `doc/spec`.
- TEST-005 | The export reconsideration left the approved spec byte-for-byte unchanged, appended
  history, reopened only the two contradicted decisions and requested resolution before editing.
- TEST-006 | The settled color-fix agent changed and checked one HTML value without creating any
  process artifact or restarting discovery.
- TEST-007 | Greenfield, tiny-fix, urgent critical migration and approved-spec change scenarios showed
  proportional ceremony while the passkey run retained blocking recovery and migration gates.
- TEST-008 | The passkey adversarial output stayed specific to enrollment, recovery, tenant
  authorization and credential retirement rather than enumerating a generic checklist.
- TEST-009 | All generated context/history artifacts were inspected; they contained structured
  evidence, decisions and deltas but no raw transcript, credential or unnecessary personal data.
  In a public-repository scenario containing a confidential customer, launch month and price, the
  agent wrote nothing and asked whether to use ignored local, generalized tracked or conversational
  memory.
- TEST-010 | Official skill validation, all 24 unit tests including 16 legacy cases, v1 ready/trace,
  and the new strict ready/trace gates passed locally on 2026-07-31.
- TEST-011 | `test_init_does_not_persist_environment_username` passed with a synthetic personal
  `USER` value and observed only `owner: "unassigned"` in the generated artifact; the ready-gate
  owner test rejected that placeholder until assigned.
- TEST-012 | Portuguese and Spanish localization tests passed critical ready gates using localized
  Given/When/Then, rollout and security terminology.
- TEST-013 | Focused tests rejected missing `should` disposition, unexplained `not-applicable`, and
  bare decisions, owner/self review and placeholder evidence, while accepting a case-insensitive
  affected-requirement rationale and independent review evidence. Trace also rejected a verified
  uncovered `should`.

- REVIEW-001 | general | passed | reviewer: final_skill_review | evidence: independent review record 2026-07-31 in docs/history/2026-07-31-conversation-first-skill.md
- REVIEW-002 | verification | passed | reviewer: validator_delta_review | evidence: validator review record 2026-07-31 in docs/history/2026-07-31-conversation-first-skill.md

## Decisions

- DEC-001 | Keep the deterministic validator CLI and Markdown grammar stable while evolving the
  human-agent operating model around it. | rationale: conversation quality is judgment-heavy, while
  the v1 grammar is already a useful invariant. | affects: REQ-004, REQ-010
- DEC-002 | Reuse established documentation paths and default only greenfield projects to singular
  `doc/`. | rationale: a universal path mandate would create duplication and contradict evidence-first
  discovery. | affects: REQ-004
- DEC-003 | Treat the approved spec as stable but revisable through an explicit reopen rather than
  technically immutable. | rationale: projects mature, but silent mutation destroys trust and
  traceability. | affects: REQ-005
- DEC-004 | Interpret value broadly and load commercial growth guidance only when the project or user
  calls for it. | rationale: open source, learning and internal tools have value propositions without
  requiring monetization. | affects: REQ-003
- DEC-005 | Keep critical safety, privacy and recovery decisions firm while making the surrounding
  interaction advisory. | rationale: flexibility cannot authorize irreversible harm or unsupported
  security claims. | affects: REQ-007, REQ-008
- DEC-006 | Supersede the v1 interaction requirement to announce mode and profile at the start while
  retaining those fields in formal artifacts. | rationale: the opening should understand the idea;
  classification becomes useful when scope and risk are known. | affects: REQ-002, REQ-006, REQ-010
- DEC-007 | Correct deterministic false passes, localized keyword false failures and implicit
  environment-owner retention without expanding the CLI. | rationale: preserving a known mismatch
  would contradict the public contract and privacy model; focused tests bound the change. | affects:
  REQ-011, REQ-012, REQ-013

## Open Questions

- None blocking — release naming remains an operational maintainer choice after verification.
