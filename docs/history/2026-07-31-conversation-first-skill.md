# Conversation-first skill revision

Date: 2026-07-31

## Trigger

The maintainer observed that the first Evidrail skill behaved more like a fixed process than a
thinking aid. They proposed using conversation, adaptive questions and durable project memory to
help an idea mature without letting the agent specify the product on the user's behalf.

## Inputs considered

- the maintainer's requested conversational, value-focused and adversarial flow, summarized here so
  public repository evidence remains self-contained;
- the existing `spec-driven-development` skill, validator, templates and verified v1 contract;
- Matt Pocock's small, composable skills and their fact-versus-decision, dependency-tree and draft-
  before-write interaction patterns;
- Revenue-Centric Design's focus on a clear beneficiary, concrete value, proof and disciplined
  feature scope.

## Understanding reached

- Discovery begins with the value and desired experience, not with architecture or a generated
  requirements list.
- The agent researches facts independently and asks the user only about genuine choices.
- Each answer can change which question is useful next; questions arrive one at a time or as a small
  independent frontier.
- An adversarial pass follows a sufficiently understood happy path and turns credible failure or
  misuse into explicit decisions and mitigations.
- Context may evolve continuously; session history records why it changed; an approved spec changes
  only through a visible reopen, delta summary and renewed confirmation.
- The skill steps back during ordinary implementation and returns only when the implementation
  discovers drift, a material choice, a risk boundary or missing verification.

## Scope chosen

Keep the validator CLI and Markdown grammar stable. Change the skill's trigger and operating
guidance, add focused references for conversation/value and living memory, add reusable
context/history templates, update the public positioning and validate behavior with independent
scenario tests. Permit small validator corrections when an observed false pass, privacy leak or
localized false failure contradicts the documented contract.

## Deferred

- A general project-memory CLI: no deterministic need has been demonstrated.
- A cryptographic spec-sealing command: potentially useful for later drift detection, but premature
  before the lighter conversation and memory model is exercised in practice.
- Hosted collaboration, embeddings, transcript storage or a project-management board.
- Automatic monetization analysis for projects whose value is non-commercial.

## Next checkpoint

Review the revised artifacts against greenfield, small-fix, critical-change and accelerated-work
scenarios; record any behavior changes caused by those tests.

## Verification checkpoint

Six fresh-agent scenarios were completed after the first revision:

- open-source discovery created living memory, adapted value to adoption and asked one root question;
- commercial discovery used market-value language without selecting a niche or metric for the user;
- a settled color fix changed one file and created no process artifacts;
- an urgent passkey migration refused fake implementation and preserved account/recovery decisions;
- a contradictory export request updated context/history but left the approved spec unchanged;
- a confidential public-repository request wrote no memory before asking how visibility should work.

No scenario stored a raw transcript or sensitive value. The results confirmed the current scope and
did not justify adding a new CLI. Full evidence is summarized in `docs/forward-tests.md`.

An independent artifact and implementation review then identified an implicit environment-username
owner, English-only structural keywords, unexplained optional trace dispositions and an obvious
self-review false pass. The CLI surface and artifact grammar remained unchanged; focused validator
checks and tests corrected those mismatches.

Two fresh independent re-reviews reached PASS after exercising quoted and localized owner/reviewer
values, missing and punctuation-only rationales, uncovered `should` requirements, unresolved review
prose, dated reports, URLs and repeat-copy installation. The official skill validator, all 24 unit
tests, both specification gates and trace commands, Python compilation and diff hygiene passed
locally.

Next checkpoint: commit, remote CI and verified status closure.
