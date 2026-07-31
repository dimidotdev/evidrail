# Current context

Last updated: 2026-07-31

## Project snapshot

Evidrail is an open-source Codex skill plus a dependency-free validator for turning product and
engineering intent into testable specifications. Version 1 proved the artifact grammar and gates,
but its operating instructions activate too broadly and can make specification feel like a rigid
process imposed by the agent.

## Current objective

Evolve the skill into a conversation-first thinking aid that helps an idealizer mature an idea,
understand its value, expose consequential choices and preserve project memory without taking
ownership of product decisions. Once the user approves a specification, that spec becomes the
stable delivery baseline until a visible reconsideration is approved.

## Value model

- Primary beneficiary: a developer, founder, maintainer or non-technical idealizer building with
  an AI agent.
- Problem: the agent can fill ambiguity with plausible decisions, while the idea, rationale and
  changing context disappear across sessions.
- Desired outcome: fewer well-built wrong products; faster recovery of project intent; explicit
  ownership of material decisions; documentation that evolves with the project.
- Possible value signals: clearer user approval, fewer reopened decisions during implementation,
  reduced context reconstruction, traceable scope changes and useful adoption by open-source teams.
- Value is not presumed to mean revenue. It may be learning, internal leverage, public utility,
  adoption, trust, portfolio value or commercial return.

## Established constraints

- Keep the skill compact and progressively disclose detailed prompts and document conventions.
- Ask only questions unlocked by known facts; inspect the repository before asking discoverable
  questions.
- Recommend and challenge, but do not silently choose material product or architecture direction.
- Avoid interview fatigue and documentation theater; tiny settled work must remain tiny.
- Keep the existing Markdown validator and artifact grammar backward compatible.
- Preserve firm safety and recovery gates for high-risk work.
- Store structured summaries, not verbatim transcripts or secrets.

## Decision board

States: `pending`, `exploring`, `proposed`, `confirmed`, `deferred`, `superseded`.

| ID | Decision or question | State | Owner | Evidence / next step |
| --- | --- | --- | --- | --- |
| D-001 | The skill is a facilitator and knowledge base, not an autonomous product owner. | confirmed | user | Direct maintainer request summarized in the session history. |
| D-002 | Ask adaptive questions from the currently unlocked decision frontier instead of issuing a full questionnaire. | confirmed | user | Direct request; corroborated by Matt Pocock's `grilling` pattern. |
| D-003 | Start discovery with beneficiary, problem, outcome and proof of value; apply commercial lenses only when relevant. | confirmed | user | Direct request; informed by Revenue-Centric Design. |
| D-004 | Keep context mutable, history append-only and approved specifications stable until explicit reconsideration. | confirmed | user | Direct maintainer request summarized in the session history. |
| D-005 | Reuse an existing documentation convention; use `doc/{context,history,spec}` only as the greenfield default. | confirmed | user | The user proposed `doc` as a default rather than an immutable path. |
| D-006 | Preserve the v1 CLI and canonical spec grammar; improve living memory around it without adding a project-management command. | confirmed | user | The request scopes this increment to a useful skill and asks to avoid making it immense. |
| D-007 | Store concise structured summaries and exclude raw transcripts, secrets and unnecessary personal data. | confirmed | user | User requested structured summaries; privacy hardening is a necessary boundary. |
| D-008 | During implementation, consult the skill only at decision, drift, risk and verification checkpoints. | confirmed | user | Direct request that the skill not pollute the creation process continuously. |
| D-009 | Choose a public release/tag after behavior forward tests and CI pass. | deferred | maintainer | Revisit tagging after real project usage confirms the workflow. |
| D-010 | Do not add a spec-sealing or general project-memory CLI in this increment. | confirmed | agent | Git plus visible reopen is sufficient until real use demonstrates a deterministic need. |
| D-011 | Correct inherited validator contract gaps without adding commands or changing the Markdown grammar. | confirmed | agent | Independent review found false-pass/privacy/localization cases; 24 focused tests now cover them. |

## Documentation map

This repository already uses `docs/` and `specs/`, so the new workflow preserves those established
roots rather than creating a parallel `doc/` tree:

- living context: `docs/context/current.md`;
- decision board: this current-context file;
- append-only session summaries: `docs/history/`;
- approved and draft specifications: `specs/`.

For a greenfield repository without an established convention, the skill will recommend
`doc/context/`, `doc/history/` and `doc/spec/`.

## Active specification

- `specs/evidrail-conversation-first.md` — conversation-first operating model and living memory.

## Current verification state

- Revised skill passes the official skill validator.
- All 24 validator tests, including the 16 legacy cases, and both v1 ready/trace gates pass.
- The new standard-profile spec passes the strict ready gate without warnings.
- Independent behavior tests passed for open-source discovery, commercial discovery, a settled tiny
  fix, critical passkey migration under urgency, reconsideration of an approved baseline and
  confidential discovery in a public repository.
- Independent review completed; its validator and documentation findings were corrected. Two focused
  re-reviews returned PASS. Remote CI remains before verified release status.

## Next frontier

Commit and push the reviewed change, then use remote CI evidence to decide whether the
conversation-first spec can move from implemented to verified.
