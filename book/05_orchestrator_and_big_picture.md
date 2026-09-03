# Build the Orchestrator and the big picture

The `SixHatsOrchestrator` owns the workflow around the six agents.

## Step 1 — fan out

The orchestrator sends the same problem and shared context to all six agents. In the teaching implementation, this happens sequentially for simplicity; a production system may run independent agents concurrently.

## Step 2 — preserve perspective boundaries

Each response is stored under its hat name. This matters because a synthesis is more trustworthy when readers can trace a conclusion back to the perspective that raised it.

## Step 3 — compare

The orchestrator looks across the six responses for:

- facts and unknowns;
- stakeholder reactions;
- risks and safeguards;
- benefits and value;
- alternatives and experiments;
- process and decision criteria.

## Step 4 — seek the whole elephant

The synthesis intentionally adds categories that no single hat owns:

- **Cross-hat tensions** — where valid perspectives pull in different directions.
- **Shared assumptions** — beliefs that may have gone unchallenged because everyone inherited the same framing.
- **Elephants in the room** — important but unstated system issues.
- **Information gaps** — evidence that would materially change confidence.
- **Next-step experiments** — small actions that improve the model before committing heavily.

## Step 5 — avoid false consensus

A good orchestrator can conclude that the evidence is insufficient. It can also preserve a minority warning rather than averaging it away.

For consequential decisions, add human review. Multi-agent agreement is not proof of correctness: agents may share the same training biases, source gaps, prompt assumptions, or model failure modes.

## Suggested advanced pattern: critic pass

After the first synthesis, run a second targeted pass:

1. Ask White to identify unsupported claims in the synthesis.
2. Ask Black to stress-test the proposed action.
3. Ask Green for an alternative that avoids the largest risk.
4. Ask Blue whether the process has enough evidence to decide.
5. Ask the Orchestrator to revise the synthesis and show what changed.

This is a simple path from a one-shot multi-agent demo toward a more robust deliberative workflow.
