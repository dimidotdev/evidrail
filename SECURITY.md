# Security policy

Evidrail parses local Markdown and emits local text, JSON, or SARIF. It does not evaluate specification content, execute extensions, load remote resources, or send telemetry. Those properties are part of its security boundary.

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

Specification validation cannot certify that an implementation is secure. A passing gate means that required structure and trace links are present; substantive claims still require review and observed evidence.
