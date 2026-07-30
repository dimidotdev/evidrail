# Product and Design Quality

Turn each relevant concern into observable behavior, not a checkbox.

## Intent and hierarchy

- Identify the primary user, job, and success moment.
- Make one primary action visually and semantically dominant.
- Define what is visible first, discoverable later, and intentionally absent.
- State empty, first-run, loading, success, partial, error, and recovery behavior.
- Remove features that do not reinforce the outcome; every control adds permanent cognitive cost.

## Interaction

- Use semantic controls and preserve keyboard, pointer, touch, and browser-native link behavior.
- Define focus movement, focus visibility, disabled/busy behavior, cancellation, and retry.
- Prevent accidental destructive actions with confirmation, undo, versioning, or recovery proportional to harm.
- Avoid layout shift: reserve geometry for asynchronous state and give media explicit dimensions.
- Honor reduced motion; animate opacity and transform when possible.
- Preserve deep links, history, refresh, and shareable state for filters, pagination, and meaningful UI state.

## Accessibility

- Require a logical heading and landmark structure.
- Give controls accessible names and associate labels with inputs.
- Define keyboard-only completion for the primary flow.
- Announce asynchronous status and validation without stealing focus.
- Verify contrast, zoom/reflow, 320 px layouts, target sizes, and non-color cues.
- Keep decorative elements out of the accessibility tree.
- Localize dates, numbers, pluralization, direction-sensitive UI, and user-facing copy.

## Content and trust

- Prefer specific active labels over generic actions.
- Explain errors with a recovery step.
- Show proof proportionate to the promise; do not fabricate metrics or certainty.
- Keep privacy, destructive effects, irreversible outcomes, and external navigation visible at the decision point.

## Performance

- Define a budget only where performance affects the outcome: response time, interaction latency, bundle size, memory, payload, or throughput.
- Measure at the user-relevant boundary and under realistic constraints.
- Treat loading skeletons as continuity aids, not disguises for unbounded latency.

## Design disposition format

Record concise decisions:

```text
- Primary flow: ...
- Empty/loading/error/recovery: ...
- Keyboard and focus: ...
- Responsive and content extremes: ...
- Motion: ...
- Performance budget: ...
```

For a non-visual change, use `N/A — no user interface or content behavior changes; API error semantics are covered by REQ-004` rather than a bare `N/A`.
