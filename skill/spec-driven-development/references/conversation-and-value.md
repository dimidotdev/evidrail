# Conversation and Value Discovery

Use this reference while the problem, audience, outcome or scope is still genuinely open. It is a
prompt library, not a questionnaire. Select the smallest useful branch.

## Separate facts from decisions

1. Research facts available from the repository, tests, analytics, documentation or tools.
2. List only unresolved decisions that materially affect value, behavior, scope, risk, cost or
   compatibility.
3. Draw their dependencies mentally or in the decision board.
4. Ask the root question whose answer unlocks the most useful next branch.
5. Recompute after the answer; do not continue down a stale prepared list.

Repository conventions are evidence of the current system, not proof that the user wants to retain
them. A recommendation is not confirmation.

## Choose the value language that fits

| Value mode | Useful proof examples |
| --- | --- |
| Personal or learning | capability gained, task completed, concept demonstrated, time willingly invested |
| Internal or operational | cycle time, errors, toil, handoffs, reliability, decision quality |
| Open source or public good | adoption, repeated use, contributors, interoperability, trust, saved effort |
| Portfolio or reputation | credible demonstration, technical depth, explainability, relevance to the intended audience |
| Commercial | willingness to pay, activation, conversion, retention, expansion, support burden, sustainable distribution |

Do not force commercial metrics onto another value mode. When commercial value is relevant, avoid
equating a large possible audience with a viable first audience.

## Ask by unlocked frontier

### Purpose frontier

- Who experiences the problem most clearly?
- What are they trying to accomplish, independent of the proposed solution?
- What happens today, and what is costly, frustrating, risky or impossible about it?
- Why is this worth changing now?

### Outcome frontier

- What should the person be able to do or feel afterward that they cannot today?
- What is the earliest moment at which the product proves its value?
- What observation would make you say the first version worked?
- Which promise must the project be able to demonstrate rather than merely claim?

### Scope frontier

- If only one capability could remain, which one carries the core promise?
- What looks attractive but does not deserve its permanent cognitive, operational and maintenance
  cost yet?
- What must the product never do or become?
- Which assumption can be tested with a smaller version before building the full idea?

### Experience frontier

- Walk through the first successful use as a short story. What happens first, next and at the proof
  moment?
- Which parts should be obvious by default, and which belong behind progressive disclosure?
- What should remain familiar because users already rely on it?
- Which concrete alternatives would help the user compare meaningfully different experiences?

### Sustainability frontier

Use only when relevant:

- How will the intended user discover and start using it?
- What makes them return, recommend, contribute or pay?
- What ongoing support or operational cost does each proposed feature create?
- What evidence would justify expanding beyond the first focused audience?

## Recommend without taking over

Use this shape for a consequential branch:

```text
What I found: <evidence>
Decision that remains yours: <question>
My recommendation: <option>, because <reason>
Meaningful tradeoff: <consequence>
Alternative: <genuinely different option>
```

Make the recommended choice easy to accept, but preserve an override or hybrid. Avoid presenting
three cosmetic variants as meaningful choice.

## Challenge after understanding

Once the intended successful flow is clear, ask a small number of adversarial questions tied to it:

- What if the actor is mistaken, malicious or interrupted?
- What if the dependency is slow, unavailable or inconsistent?
- What data or trust would be painful to expose or lose?
- What would make this feature expensive to support forever?
- What must remain recoverable if the chosen path fails?

Do not enumerate every theoretical threat. Escalate a finding only when it changes a decision,
requirement, verification method or explicit residual risk.

## Stop before interview fatigue

Discovery is sufficient when the following are known well enough to act:

- beneficiary and meaningful problem;
- desired outcome and proof;
- core path and non-goals;
- material constraints and confirmed decisions;
- credible failure/risk posture;
- open decisions classified as blocking, safe to defer or delegated;
- verification path.

Every additional question must retire a named material uncertainty. Otherwise summarize and ask for
baseline confirmation.

## Source influence

The dependency-tree questioning pattern is informed by
[Matt Pocock's small composable skills](https://github.com/mattpocock/skills), especially `grilling`
and `domain-modeling`. The optional focus, proof and feature-cost prompts are informed by
[Revenue-Centric Design](https://github.com/heliocosta-dev/revenue-centric-design): value and
business should reinforce each other when a business model exists. That upstream material explicitly
excludes gambling, betting and casino use; do not load or apply its commercial tactics to those
products.
