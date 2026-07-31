# Evidrail

Evidrail is an open-source, conversation-first Codex skill and dependency-free validator for
spec-driven software delivery. It helps a person mature an idea through adaptive questions, keeps
project context alive across sessions, and turns only approved decisions into a testable delivery
contract.

It is designed for the uncomfortable middle between “just prompt the model” and a heavyweight RFC process:

- the agent discovers facts but the idealizer retains ownership of consequential decisions;
- questions follow the currently unlocked decision frontier instead of a fixed questionnaire;
- personal, internal, open-source and commercial projects can define value in their own terms;
- living context and structured history evolve while an approved spec stays stable until explicitly
  reconsidered;
- evidence, assumptions, proposals and confirmed decisions remain visibly different;
- light, standard, and critical profiles scale with risk rather than diff size;
- product design, accessibility, security, privacy, reliability, and recovery shape the behavior early;
- deterministic gates catch placeholders, blocking questions, malformed requirements, orphaned acceptance criteria, and missing test coverage;
- plain Markdown remains the source of truth.

## Why Evidrail

Generated code can be internally coherent and still solve the wrong problem. More prompting does
not repair an undefined outcome, an agent-made product decision, an invisible trust boundary or
project context that vanished between sessions.

Evidrail combines two parts:

1. **`spec-driven-development` skill** — facilitates value and behavior discovery, preserves living
   context, challenges the emerging design and steps back once the approved baseline is clear.
2. **`evidrail.py`** — initializes the artifact and enforces the portions that should not depend on judgment.

The validator does not certify that a design is good or a system is secure. It makes unsupported claims and missing links harder to hide.

## Quick start

Requirements: Python 3.11 or newer for the optional validator. No third-party runtime package is
used.

Start by invoking the skill before generating a spec:

```text
Use $spec-driven-development to help me mature this idea. Ask only the next useful questions and do
not decide product direction for me.
```

For an ongoing writable project, the skill reuses the repository's existing documentation paths. In
a greenfield repository it defaults to `doc/context`, `doc/history`, and—only after the idea has
converged—`doc/spec`.

When the proposed baseline has been summarized and approved, initialize the formal artifact:

```bash
git clone https://github.com/dimidotdev/evidrail.git /path/to/evidrail
cd /path/to/your-product
python3 /path/to/evidrail/skill/spec-driven-development/scripts/evidrail.py init doc/spec/my-change.md \
  --title "My change" --profile standard --mode deliver --owner "my-team"
```

Fill the generated artifact, then run:

```bash
python3 /path/to/evidrail/skill/spec-driven-development/scripts/evidrail.py check doc/spec/my-change.md --gate ready
python3 /path/to/evidrail/skill/spec-driven-development/scripts/evidrail.py trace doc/spec/my-change.md
```

After implementation, record real verification results, set `status: verified`, and run:

```bash
python3 /path/to/evidrail/skill/spec-driven-development/scripts/evidrail.py check doc/spec/my-change.md --gate verified
```

Use `--format json` or `--format sarif` with `check` for automation. Use `--strict` to make warnings fail non-critical specifications; ready and verified critical profiles already fail on warnings.

## Install the Codex skill

Copy or link `skill/spec-driven-development` into your Codex skills directory:

```bash
skill_destination="$HOME/.codex/skills/spec-driven-development"
mkdir -p "$skill_destination"
cp -R skill/spec-driven-development/. "$skill_destination/"
```

PowerShell:

```powershell
$skillDestination = "$HOME/.codex/skills/spec-driven-development"
New-Item -ItemType Directory -Force $skillDestination | Out-Null
Copy-Item -Recurse -Force "skill/spec-driven-development/*" $skillDestination
```

Then invoke it explicitly:

```text
Use $spec-driven-development to help me explore this change, preserve its context, and formalize only
the decisions I approve.
```

The skill is active during discovery, formalization, material reconsideration and closure. It stays
in the background during routine implementation with settled requirements. Formal specs still
support three modes:

- `specify`: produce and validate the contract without changing product code;
- `deliver`: carry the change from evidence through verified implementation;
- `audit`: compare intent, implementation, and evidence.

Profiles are independent of change size: `light`, `standard`, and `critical`. They scale depth rather
than replace judgment. Authentication, authorization, secrets, sensitive data, money, destructive
actions, migrations, untrusted execution, and broad infrastructure remain critical even when the
diff is small.

## Artifact contract

Specifications use scalar frontmatter, canonical H2 sections, stable IDs, and a trace table:

```text
REQ-001 -> AC-001 -> TEST-001 -> passed
```

Normative levels are `must`, `must-not`, `should`, and `may`. Ready specifications require
acceptance and planned verification for every `must` and `must-not`. Verified specifications require
passed evidence for those release requirements and a passed or explicitly explained disposition for
every `should`; `may` remains optional. `init` uses the privacy-safe placeholder owner `unassigned`
when `--owner` is omitted, but ready and verified gates require replacing it with an explicit team or
person.

See [`specs/evidrail-v1.md`](specs/evidrail-v1.md) for the original validator contract and
[`specs/evidrail-conversation-first.md`](specs/evidrail-conversation-first.md) for the conversational
operating model. The current project memory lives in [`docs/context/current.md`](docs/context/current.md),
and independent behavior-test iterations are recorded in
[`docs/forward-tests.md`](docs/forward-tests.md).

## Development

```bash
python3 -m unittest discover -s tests -v
python3 skill/spec-driven-development/scripts/evidrail.py check specs/evidrail-v1.md --gate ready
python3 skill/spec-driven-development/scripts/evidrail.py check specs/evidrail-conversation-first.md --gate ready --strict
```

The CI matrix runs on Linux, Windows, and macOS.

Contributions are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing the artifact contract or a validation rule.

## License

MIT © Matheus Silva
