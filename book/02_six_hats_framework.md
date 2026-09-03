# The Six Thinking Hats as agent roles

Edward de Bono's Six Thinking Hats is a **parallel thinking** method: deliberately separate modes of thinking so each can receive focused attention rather than mixing facts, feelings, criticism, optimism, creativity, and process control into one argument.

For this project, each hat becomes an agent specialization.

## White Hat — information

**Mission:** identify what is known, what is claimed, what is missing, and what evidence would reduce uncertainty.

Agent behaviors:
- separate observations from assumptions;
- identify data quality and provenance questions;
- list missing facts;
- avoid inventing evidence.

## Red Hat — feelings and intuition

**Mission:** surface emotional reactions, intuitions, stakeholder sentiment, and unease that may not yet be captured by formal analysis.

Agent behaviors:
- label feelings as feelings, not facts;
- include possible stakeholder reactions;
- avoid forcing emotional claims to masquerade as evidence.

## Black Hat — caution

**Mission:** identify risks, failure modes, constraints, and reasons a proposal may not work.

Agent behaviors:
- make risks specific;
- connect each risk to a mechanism or condition;
- avoid reflexive pessimism.

## Yellow Hat — benefits and value

**Mission:** identify benefits, opportunities, strengths, and reasons a proposal may work.

Agent behaviors:
- make value claims testable when possible;
- distinguish immediate gains from longer-term value;
- avoid unsupported cheerleading.

## Green Hat — creativity

**Mission:** generate alternatives, reframings, experiments, combinations, and novel options.

Agent behaviors:
- produce multiple options before selecting one;
- challenge hidden constraints;
- turn objections into design prompts.

## Blue Hat — process control

**Mission:** improve the *thinking process itself*.

Agent behaviors:
- clarify the decision question;
- propose sequence and scope;
- define decision criteria;
- identify which hat should be revisited and why;
- summarize what the thinking process still needs.

## Why keep a separate Orchestrator?

The Blue Hat participates as a perspective. The Orchestrator owns the software workflow: calling agents, collecting structured outputs, preserving traceability, and building a cross-perspective synthesis. This separation makes the implementation easier to inspect and extend.

## Sources

- Edward de Bono, *Six Thinking Hats*: https://www.debono.com/Books/six-thinking-hats
- De Bono Group overview of the six roles: https://www.debonogroup.com/services/core-programs/six-thinking-hats/
