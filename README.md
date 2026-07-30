# Evidrail

Evidrail is an open-source Codex skill and dependency-free validator for spec-driven software delivery. It turns intent into an evidence-backed contract before implementation, then keeps requirements connected to acceptance criteria and actual verification.

It is designed for the uncomfortable middle between “just prompt the model” and a heavyweight RFC process:

- evidence, assumptions, and decisions remain visibly different;
- light, standard, and critical profiles scale with risk rather than diff size;
- product design, accessibility, security, privacy, reliability, and recovery shape the behavior early;
- deterministic gates catch placeholders, blocking questions, malformed requirements, orphaned acceptance criteria, and missing test coverage;
- plain Markdown remains the source of truth.

## Why Evidrail

Generated code can be internally coherent and still solve the wrong problem. More prompting does not repair an undefined outcome, an invisible trust boundary, or acceptance criteria that were never written.

Evidrail combines two parts:

1. **`spec-driven-development` skill** — guides discovery, risk classification, design, implementation, and evidence-based closure.
2. **`evidrail.py`** — initializes the artifact and enforces the portions that should not depend on judgment.

The validator does not certify that a design is good or a system is secure. It makes unsupported claims and missing links harder to hide.

## Quick start

Requirements: Python 3.11 or newer. No third-party runtime package is used.

```bash
git clone https://github.com/dimidotdev/evidrail.git
cd evidrail
python3 skill/spec-driven-development/scripts/evidrail.py init specs/my-change.md \
  --title "My change" --profile standard --mode deliver --owner "my-team"
```

Fill the generated artifact, then run:

```bash
python3 skill/spec-driven-development/scripts/evidrail.py check specs/my-change.md --gate ready
python3 skill/spec-driven-development/scripts/evidrail.py trace specs/my-change.md
```

After implementation, record real verification results, set `status: verified`, and run:

```bash
python3 skill/spec-driven-development/scripts/evidrail.py check specs/my-change.md --gate verified
```

Use `--format json` or `--format sarif` with `check` for automation. Use `--strict` to make warnings fail non-critical specifications; ready and verified critical profiles already fail on warnings.

## Install the Codex skill

Copy or link `skill/spec-driven-development` into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skill/spec-driven-development ~/.codex/skills/spec-driven-development
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME/.codex/skills" | Out-Null
Copy-Item -Recurse skill/spec-driven-development "$HOME/.codex/skills/spec-driven-development"
```

Then invoke it explicitly:

```text
Use $spec-driven-development to specify and deliver this change.
```

The skill supports three modes:

- `specify`: produce and validate the contract without changing product code;
- `deliver`: carry the change from evidence through verified implementation;
- `audit`: compare intent, implementation, and evidence.

Profiles are independent of change size: `light`, `standard`, and `critical`. Authentication, authorization, secrets, sensitive data, money, destructive actions, migrations, untrusted execution, and broad infrastructure are critical even when the diff is small.

## Artifact contract

Specifications use scalar frontmatter, canonical H2 sections, stable IDs, and a trace table:

```text
REQ-001 -> AC-001 -> TEST-001 -> passed
```

Normative levels are `must`, `must-not`, `should`, and `may`. Ready specifications require acceptance and planned verification for every `must` and `must-not`; verified specifications require passed evidence.

See [`specs/evidrail-v1.md`](specs/evidrail-v1.md) for the project dogfooding its own contract.
The independent behavior-test iterations and the changes they caused are recorded in [`docs/forward-tests.md`](docs/forward-tests.md).

## Development

```bash
python3 -m unittest discover -s tests -v
python3 skill/spec-driven-development/scripts/evidrail.py check specs/evidrail-v1.md --gate ready
```

The CI matrix runs on Linux, Windows, and macOS.

Contributions are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing the artifact contract or a validation rule.

## License

MIT © Matheus Silva
