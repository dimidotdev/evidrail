# Security policy

Evidrail parses local Markdown and emits local text, JSON, or SARIF. It does not evaluate
specification content, execute extensions, load remote resources, or send telemetry. Those
properties are part of its security boundary.

The skill may guide an authorized agent to maintain local context and structured history. These
files are ordinary project documentation, not a private vault: do not store raw transcripts,
credentials, tokens, OTPs, private keys, unnecessary personal data, or production artifacts in
them. Before persisting confidential roadmap, customer or business context, inspect whether the
destination is tracked, ignored and likely public; ask whether it should be generalized, stored
locally under an existing ignore policy, or not persisted. Do not silently add ignore rules or rely
on current repository privacy as a permanent guarantee.

## Supported versions

Security fixes are applied to the latest tagged release. This project is pre-1.0; review release notes before upgrading because the artifact contract may still evolve.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting for `dimidotdev/evidrail` when available. If that channel is unavailable, email `contact@dimi.dev.br` with:

- the affected version and platform;
- the smallest reproducible input;
- expected and observed behavior;
- impact and any known workaround.

Do not include real credentials, personal data, or production artifacts. You should receive an acknowledgement within seven days. No bounty or guaranteed remediation timeline is offered.

## Scope notes

Specification validation cannot certify that an implementation is secure. A passing gate means that
required structure and trace links are present; substantive claims still require review and observed
evidence. A recorded decision state is not proof of the decision maker's identity or authorization;
teams that require authenticated approval should use their existing signed review or governance
system.
