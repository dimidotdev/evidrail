# Contributing to Evidrail

Thanks for helping make AI-assisted delivery more deliberate and verifiable.

## Before changing behavior

1. Inspect and update `docs/context/current.md` when the change alters current direction or constraints.
2. Record material decision changes on the current-context decision board and in a concise
   `docs/history/` checkpoint; do not copy raw conversations or sensitive values.
3. Open or update a specification under `specs/` when behavior or the public artifact contract
   changes, and confirm consequential product decisions before marking it ready.
4. Separate observed evidence, assumptions, proposals, and confirmed decisions.
5. Add a fixture, behavior test, or unit test at the boundary actually changed.
6. Keep the validator dependency-free unless a specification demonstrates why that constraint no
   longer serves users.

## Local checks

```bash
python3 -m unittest discover -s tests -v
python3 skill/spec-driven-development/scripts/evidrail.py check specs/evidrail-v1.md --gate ready
python3 skill/spec-driven-development/scripts/evidrail.py check specs/evidrail-conversation-first.md --gate ready --strict
python3 skill/spec-driven-development/scripts/evidrail.py trace specs/evidrail-v1.md
python3 skill/spec-driven-development/scripts/evidrail.py trace specs/evidrail-conversation-first.md
```

Run the equivalent commands with `python` on Windows.

## Design principles

- Prefer observable behavior over implementation prescriptions.
- Scale ceremony with risk, not with lines changed.
- Keep judgment in the skill and deterministic invariants in the validator.
- Ask only material questions that repository evidence cannot answer, and preserve user decision
  ownership.
- Treat the greenfield `doc/` layout as a default, not a reason to replace an established convention.
- Do not weaken a gate only to make an artifact pass.
- Preserve stable finding codes once released; document any unavoidable breaking change.
- Treat skipped checks and unsupported claims as gaps, not successful evidence.

## Pull requests

Describe the user outcome, affected requirement IDs, tests run, and residual risk. A security-sensitive change should receive an independent review and include negative-path evidence.
