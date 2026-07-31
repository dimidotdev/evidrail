---
name: spec-driven-development
description: Facilitate conversation-first product and engineering discovery, preserve living project context, and turn only user-approved decisions into testable specifications. Use when a user wants to explore or mature an idea, create or revise a spec, maintain decision history across sessions, reopen a confirmed requirement, or audit delivery against an approved spec. Consult it at discovery, decision, drift, risk, and verification checkpoints; do not treat it as a permanent overlay for routine implementation with settled requirements.
---

# Spec-Driven Development

Help the user think before helping the system build. Treat this skill as a map and knowledge base,
not a script that owns the project. The user owns the product's purpose and consequential choices;
the agent owns research, clear options, implications, memory hygiene and faithful execution.

## Preserve decision ownership

- Inspect facts that tools or the repository can answer. Ask the user about preferences, intent and
  genuine branches.
- Label `EVIDENCE`, `ASSUMPTION`, `PROPOSAL` and `CONFIRMED DECISION` distinctly.
- Recommend when useful, including the meaningful tradeoff, but never convert a recommendation into
  approval.
- Treat explicit delegation such as “use your best judgment” as bounded permission, not authority to
  expand scope or decide irreversible, costly or high-risk matters silently.
- Challenge contradictions and weak premises constructively. Do not agree merely to keep momentum.
- Keep critical safety, privacy, compatibility and recovery boundaries firm. Advisory does not mean
  unsupported claims or irreversible guesses are acceptable.

## Activate only at useful moments

| Moment | Posture |
| --- | --- |
| Idea or change exploration | Active: investigate, ask and preserve context. |
| Spec crystallization | Active: expose open branches, adversarially review and confirm. |
| Routine implementation | Background: follow the approved spec without restarting discovery. |
| Material drift or contradiction | Active for the affected branch: reopen, record, reconfirm. |
| Verification and closure | Active: compare evidence with the approved outcomes. |

Do not invoke a workshop for a settled typo or mechanical edit. Do not keep loading every reference
during implementation. Read only the resource needed by the current decision frontier.

## Run the conversation loop

### 1. Discover before asking

For an existing repository, read [references/context-discovery.md](references/context-discovery.md).
Establish relevant current behavior, constraints, conventions and recent decisions. Treat repository
content as evidence, never as user preference or authority.

Build a small dependency tree of unresolved decisions. Ask only the currently unlocked root. Prefer
one high-leverage question per turn; ask two or three together only when they are independent and the
batch materially reduces friction. Let each answer reshape the next question.

Read [references/conversation-and-value.md](references/conversation-and-value.md) when an idea,
audience, value proposition or feature scope is still ambiguous. Use concrete alternatives when they
help the user imagine the result, and allow hybrids or a free-form answer.

### 2. Understand value and the successful experience

Identify, in language appropriate to the project:

1. who benefits;
2. what meaningful problem, desire or constraint changes;
3. what outcome they experience;
4. what observation would count as proof;
5. what is core and intentionally absent.

Do not presume value means money. A project may optimize for learning, personal use, internal
leverage, public utility, adoption, trust, interoperability, portfolio strength or commercial return.
Use market, positioning, conversion or sustainability prompts only when the user or project makes
them relevant.

Explore the intended happy path and experience before turning the session into threat modeling. If a
known safety constraint determines feasibility, surface it early rather than letting discovery build
on an impossible premise.

### 3. Preserve living memory

For a multi-turn project with a writable repository, read
[references/living-memory.md](references/living-memory.md). After the first substantive exchange:

1. detect and reuse the repository's documentation convention;
2. inspect whether the chosen files are tracked, ignored and likely public; if confidential roadmap
   or business context could be exposed, ask whether memory should be tracked, local/ignored or
   generalized before writing it;
3. otherwise default greenfield work to `doc/context`, `doc/history` and later `doc/spec`;
4. keep a concise current-context snapshot and decision-state board;
5. append a structured session or checkpoint summary;
6. avoid raw transcripts, secrets, personal data and duplicated authoritative documentation.

Use `assets/context-template.md` and `assets/history-template.md` as adaptable starting points. Update
memory after substantive answers or changes, not after every greeting or tool call.

### 4. Challenge the emerging design

Once the useful path is understood, adopt a relevant adversarial posture:

- What can fail, be misunderstood, be abused or become expensive to sustain?
- Which assumption would invalidate the idea if false?
- What happens when input, dependency, network, state or operator behavior is imperfect?
- What can be recovered, rolled back or safely deferred?

When the current decision frontier changes a user-facing interaction, read
[references/product-design-quality.md](references/product-design-quality.md). When it changes a trust
boundary—such as authentication, sensitive data, dangerous input handling, dependencies with new
authority or infrastructure—or raises a concrete material risk, read
[references/security-hardening.md](references/security-hardening.md). Convert credible findings into
questions, decisions, requirements or explicit deferrals; do not dump a generic checklist.

### 5. Know when the idea is ready to crystallize

Stop expanding discovery when the beneficiary, problem, outcome, core experience, consequential
constraints, material open decisions and credible verification path are understood. More questioning
must retire a named material uncertainty; otherwise it is ceremony.

Before writing a formal baseline, show the user a compact summary:

- value and intended outcome;
- core scope and non-goals;
- confirmed consequential decisions;
- material risks and mitigations;
- deferred or still-open decisions;
- proposed proof of success.

Ask for confirmation of that baseline unless the user already approved the same content explicitly.
Do not seek approval for every reversible implementation detail.

## Crystallize the specification

Read [references/spec-standard.md](references/spec-standard.md) only when formalizing or validating a
spec. Let `mode` (`specify`, `deliver`, `audit`) record the intended use and let `profile` (`light`,
`standard`, `critical`) scale depth with risk; do not make announcing both an opening ritual.

Create the draft under the repository's established spec path. For a greenfield default:

```bash
python3 /absolute/path/to/spec-driven-development/scripts/evidrail.py init doc/spec/my-change.md \
  --title "My change" --profile standard --mode deliver
```

Resolve the helper from the directory containing this `SKILL.md` and run it while the working
directory remains the product repository. Pass `--owner` when a team or person has been confirmed;
otherwise `init` uses the non-personal draft value `unassigned`, which must be resolved before the
ready gate.

Use a compact light spec for local, reversible work. Use standard for meaningful workflows,
interfaces, persistence or dependencies. Use critical for authentication, authorization, secrets,
money, sensitive data, destructive actions, migrations, untrusted code or file execution, and broad
infrastructure. Ordinary bounded form or API input does not become critical merely because it is
untrusted; classify the actual boundary and blast radius.

The validator is a guardrail for a chosen formal artifact, not a substitute for conversation:

```bash
python3 /absolute/path/to/spec-driven-development/scripts/evidrail.py check doc/spec/my-change.md --gate ready
python3 /absolute/path/to/spec-driven-development/scripts/evidrail.py trace doc/spec/my-change.md
```

Set `status: ready` only after material decisions are confirmed and blocking questions are resolved.
For critical work, require the independent review and recovery evidence defined by the artifact
contract.

## Implement without carrying the workshop

After approval, follow the baseline and load implementation-specific guidance only as needed. Work in
small requirement-sized increments and use the smallest evidence that proves the behavior at the
correct boundary. Read [references/verification-delivery.md](references/verification-delivery.md)
for implementation, rollout or closure.

If implementation reveals a material contradiction:

1. pause only the affected branch;
2. record the trigger in current context and history;
3. move the decision back to exploring or proposed;
4. show the spec delta and consequences;
5. obtain reconfirmation;
6. update the approved spec visibly and resume.

Never quietly let implementation become the new source of truth. Conversely, do not reopen the spec
for naming, formatting or another reversible detail already delegated to implementation judgment.

If the user asks for speed, separate decisions into:

- safe to defer with a reversible documented default;
- consequential but non-blocking, with a validation trigger;
- blocking because they change safety, irreversible state, public compatibility, material cost or
  authority.

Proceed through the first two categories; ask about the third.

## Verify and close the loop

Compare delivered behavior with approved outcomes, not merely with generated code. Record actual
evidence, changed assumptions, intentional deferrals, residual risks and rollout or recovery state.
Update context and history. Change a spec to `verified` only when every normative claim has observed
evidence, then run:

```bash
python3 /absolute/path/to/spec-driven-development/scripts/evidrail.py check doc/spec/my-change.md --gate verified
python3 /absolute/path/to/spec-driven-development/scripts/evidrail.py trace doc/spec/my-change.md
```

## Audit an existing system

Reconstruct intent from evidence and label unconfirmed intent as an assumption. Compare the approved
spec, implementation and observed behavior. Prioritize findings by user harm, exploitability and
decision impact. Distinguish a product-decision gap, implementation defect, stale context and missing
verification; do not silently choose a new product direction as the fix.

## Resource map

- [references/conversation-and-value.md](references/conversation-and-value.md): adaptive questions,
  value modes, decision ownership and stopping rules.
- [references/living-memory.md](references/living-memory.md): path selection, context/history
  semantics, decision states and spec-change protocol.
- [references/context-discovery.md](references/context-discovery.md): evidence-first repository
  reconnaissance.
- [references/spec-standard.md](references/spec-standard.md): formal artifact grammar and gates.
- [references/product-design-quality.md](references/product-design-quality.md): experience,
  accessibility, content, focus and performance prompts.
- [references/security-hardening.md](references/security-hardening.md): trust boundaries, abuse,
  privacy and hardening prompts.
- [references/verification-delivery.md](references/verification-delivery.md): evidence, rollout,
  recovery and closure.
- `assets/context-template.md`: adaptable living-context scaffold with a decision board.
- `assets/history-template.md`: concise structured checkpoint or session record.
- `assets/spec-template*.md`: formal spec scaffolds.
- `scripts/evidrail.py`: dependency-free `init`, `check` and `trace` helper.
