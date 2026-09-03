# What are agents and orchestrators?

An **agent** is more than a one-off prompt. For this project, an agent has four pieces:

1. **Role** — what perspective it is responsible for.
2. **Instructions** — what it should pay attention to and what it should avoid doing.
3. **Input contract** — the problem, shared context, and any constraints.
4. **Output contract** — a predictable structure that another component can consume.

A production AI agent may also have tools, memory, retrieval, planning loops, approvals, and external actions. We start smaller so the mechanics are visible.

## Orchestration

The **Orchestrator** coordinates multiple agents. Its job is not merely to concatenate six answers. It should:

- invoke the agents consistently;
- keep their perspectives distinguishable;
- compare overlap and disagreement;
- identify missing evidence and untested assumptions;
- ask whether one perspective is dominating;
- synthesize a decision-oriented view;
- propose next questions, experiments, or actions.

## Parallel first, synthesis second

A useful pattern is to have the hats work **independently on the same initial prompt** before they see one another's answers. This reduces premature convergence and gives the orchestrator genuinely different observations to compare.

A second pass can then be added later: selected hats critique the synthesis, or the orchestrator asks for targeted follow-up on a contradiction.

## A reusable mental model

```text
problem + shared context
        |
        v
  ┌─────────────┐
  │ Orchestrator│
  └──────┬──────┘
         |
         +--> White
         +--> Red
         +--> Black
         +--> Yellow
         +--> Green
         +--> Blue
         |
         v
compare -> blind spots -> synthesis -> next steps
```

In Notebook 1 you will inspect the role prompts and run the six agents. In Notebook 2 you will focus on the orchestration logic.
