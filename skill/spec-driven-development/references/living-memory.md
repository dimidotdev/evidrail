# Living Project Memory

Use living memory to prevent context loss, not to manufacture paperwork. Keep the smallest set of
files that lets a future collaborator recover what the project is, why it changed and which decisions
are authoritative.

## Select paths without creating a second system

Inspect the repository first:

1. If it already has a documentation and spec convention, reuse it.
2. If paths exist but their purpose is ambiguous, ask before reorganizing.
3. If it is greenfield and the user wants ongoing specification, default to:

```text
doc/
├── context/
│   └── current.md
├── history/
│   └── YYYY-MM-DD-<topic>.md
└── spec/
    └── <slug>.md
```

Keep the decision board in `current.md` for a small project. Split it to
`context/decisions.md` only when the current snapshot becomes hard to scan. Do not migrate existing
`docs/`, `specs/`, ADRs or issue trackers merely to match this default.

Before the first persistent write, inspect Git status, ignore rules, remotes and repository
documentation well enough to understand likely visibility. If a public or tracked destination could
expose confidential roadmap, customer or business context, ask the user to choose one of:

- tracked project memory with generalized sensitive details;
- local ignored memory;
- no persistent memory, with a concise in-conversation handoff instead.

Do not silently add ignore rules or assume that a private repository will remain private.

## Give each artifact one job

### Current context — mutable

Answer what a new session needs now:

- project snapshot and current stage;
- beneficiary, problem, value mode and proof;
- active scope, constraints and non-goals;
- active spec links;
- known risks and next decision frontier;
- decision board.

Rewrite stale statements instead of accumulating a chronology here. Link to authoritative code or
docs rather than duplicating them.

### History — append-only summaries

Record why the current state changed:

- trigger or question;
- new evidence and user answers;
- decisions confirmed, reopened, deferred or superseded;
- material spec/context deltas;
- unresolved threads and next checkpoint.

Use one record per meaningful session or decision checkpoint. Append to the same day's topic record
when appropriate. Do not store the raw conversation.

### Specification — stable after approval

A draft is exploratory. A `ready` or otherwise approved spec is the delivery baseline. Preserve stable
IDs and make material changes visible through explicit decisions and history. Git provides file
history; do not create copied `final-v2-really-final` files.

## Track decision state

Use only the states the project needs:

| State | Meaning |
| --- | --- |
| `pending` | Known question with no active exploration yet. |
| `exploring` | Evidence or alternatives are being gathered. |
| `proposed` | A recommendation exists but lacks user confirmation. |
| `confirmed` | The authorized owner accepted the decision. |
| `deferred` | Intentionally postponed with a trigger for return. |
| `superseded` | Replaced by a later confirmed decision; retain the link. |

Record owner, rationale or evidence, and next step. Do not mark `confirmed` merely because the agent
implemented an option.

## Update cadence

Update current context and the decision board after a substantive answer, confirmed change or newly
discovered contradiction. Write a history checkpoint when one of these occurs:

- the value or scope becomes clearer;
- a material decision changes state;
- a draft becomes approved;
- implementation forces reconsideration;
- a session hands off or closes.

Do not write after greetings, status polls, repeated tool output or unchanged waiting periods.

## Reopen an approved decision

When new intent or evidence contradicts the baseline:

1. identify the affected `REQ-*`, `DEC-*` or documented behavior;
2. pause only work that depends on it;
3. record the trigger and move the decision to `exploring`;
4. present old behavior, proposed behavior, consequences and verification delta;
5. obtain confirmation;
6. update spec, context and history together;
7. mark the prior decision superseded when useful and resume.

A typo, internal name or reversible implementation choice within delegated boundaries does not need
this ceremony.

## Minimize and protect memory

- Summarize decisions and rationale; never persist raw transcripts by default.
- Exclude passwords, tokens, private keys, OTPs, personal addresses and unrelated personal details.
- Generalize sensitive business facts when exact values are not needed for future decisions.
- Do not paste large logs, source files or third-party documents; link or cite the relevant fragment.
- Respect ignored/local-only documentation and user ownership. Do not commit it without authority.
- Treat visibility as a decision: before persisting confidential roadmap or business context, confirm
  whether the destination is tracked/public, local/ignored or intentionally generalized.
- If the repository is read-only or the user requested advice only, keep a concise handoff in the
  response instead of creating files.

## Keep files bounded

When current context becomes difficult to scan, remove obsolete detail after preserving the reason in
history. When history grows, index it by date or topic; do not summarize summaries repeatedly. Specs
remain organized by independently deliverable change.
