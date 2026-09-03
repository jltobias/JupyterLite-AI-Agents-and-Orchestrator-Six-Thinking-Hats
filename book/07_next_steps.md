# Next steps: from teaching agents to real AI agents

Once the browser-safe version makes sense, extend it in layers.

## Level 1 — richer structured outputs

Replace free-form strings with fields such as:

```python
{
    "observations": [...],
    "questions": [...],
    "confidence": 0.0,
    "evidence_needed": [...],
    "recommended_next_step": "..."
}
```

Structured outputs make orchestration, comparison, and evaluation easier.

## Level 2 — a real LLM backend

Implement the `CallableBackend` using a secure server-side endpoint. Keep the hat prompts and orchestrator unchanged.

## Level 3 — tools and retrieval

Give specific agents only the tools they need:

- White Hat: search, databases, documents, citations.
- Black Hat: policy/rule checks, dependency analysis, test results.
- Green Hat: retrieval of analogous solutions or design patterns.
- Blue Hat: task state, agenda, decision criteria, and completion checks.

Tool permissions should be narrow. An agent that only needs to read should not receive write access.

## Level 4 — memory and state

Store:

- the original problem statement;
- shared context;
- each hat's outputs;
- evidence and citations;
- unresolved questions;
- decisions and reasons;
- what changed between deliberation rounds.

This creates an auditable decision trail rather than a disappearing chat transcript.

## Level 5 — evaluation

Test the system with a reusable problem set. Score whether it:

- keeps hats in role;
- distinguishes evidence from inference;
- produces genuinely different perspectives;
- catches known planted risks or blind spots;
- preserves minority concerns;
- avoids fabricated facts;
- produces useful next questions;
- improves decisions compared with a single-agent baseline on a fixed evaluation set.

## A final design principle

The goal is not to make seven agents agree. The goal is to make the **decision process see more of the elephant** before action is taken.
