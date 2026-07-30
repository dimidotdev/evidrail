# Contributing to Evidrail

Thanks for helping make AI-assisted delivery more deliberate and verifiable.

## Before changing behavior

1. Open or update a specification under `specs/` when behavior or the public artifact contract changes.
2. Separate observed evidence, assumptions, and decisions.
3. Add a fixture or unit test that fails for the behavior being changed.
4. Keep the validator dependency-free unless a specification demonstrates why that constraint no longer serves users.

## Local checks

```bash
python3 -m unittest discover -s tests -v
python3 skill/spec-driven-development/scripts/evidrail.py check specs/evidrail-v1.md --gate ready
python3 skill/spec-driven-development/scripts/evidrail.py trace specs/evidrail-v1.md
```

Run the equivalent commands with `python` on Windows.

## Design principles

- Prefer observable behavior over implementation prescriptions.
- Scale ceremony with risk, not with lines changed.
- Keep judgment in the skill and deterministic invariants in the validator.
- Do not weaken a gate only to make an artifact pass.
- Preserve stable finding codes once released; document any unavoidable breaking change.
- Treat skipped checks and unsupported claims as gaps, not successful evidence.

## Pull requests

Describe the user outcome, affected requirement IDs, tests run, and residual risk. A security-sensitive change should receive an independent review and include negative-path evidence.
