# Evidence-First Context Discovery

## Existing repository

Inspect only what is relevant, but establish these facts before designing:

1. repository instructions and ownership boundaries;
2. worktree state and unrelated user changes;
3. entry points, data flow, and trust boundaries;
4. current behavior in code, tests, and production evidence;
5. contracts: types, schemas, routes, events, configuration, and public interfaces;
6. deployment, migration, rollback, and observability mechanisms;
7. recent history explaining why the current shape exists.

Prefer `rg` and targeted file reads. Cite sources in `EVD-*` entries, for example:

```text
- EVD-001 | source: apps/site/app/root.tsx:164 | Route status is rendered inside the flex shell.
- EVD-002 | source: production screenshot 2026-07-29 | Status text shifts content during navigation.
```

## Evidence hierarchy

Prefer, in order:

1. observed production behavior or repeatable test;
2. executable code and configuration;
3. contracts and schemas;
4. maintained documentation;
5. recent commit or issue context;
6. stakeholder statement;
7. assumption.

Lower-ranked evidence is not invalid; label conflicts and resolve them explicitly.

## Questions

Ask only when the answer cannot be safely discovered and materially changes the result. A blocking question usually concerns:

- irreversible or destructive state;
- public API or compatibility promise;
- security/privacy boundary;
- product behavior with multiple plausible outcomes;
- authority to affect external systems or people;
- material cost, schedule, or architecture expansion.

For non-blocking uncertainty, record:

```text
- ASM-001 | Users prefer the existing locale as default. | validation: inspect stored preference and test no-preference behavior.
```

## Greenfield work

Replace repository evidence with validated constraints: target users, environment, deployment model, data sensitivity, supported platforms, interoperability, operability, and explicit non-goals. Do not invent scale, compliance, or business requirements.
