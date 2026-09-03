# AI Agents, Orchestration, and the Six Thinking Hats

This book is a browser-based learning path for building a small **multi-agent system** around Edward de Bono's Six Thinking Hats.

The core experiment is simple: give six specialized agents the **same problem**, ask each to reason from a distinct perspective, then ask a seventh **Orchestrator** to preserve those perspectives while constructing a more complete picture.

## The seven roles

| Role | Primary responsibility |
|---|---|
| White Hat | Facts, evidence, unknowns, and information needs |
| Red Hat | Feelings, intuition, stakeholder reactions, and instinctive concerns |
| Black Hat | Risks, failure modes, constraints, and cautions |
| Yellow Hat | Benefits, value, opportunities, and reasons an idea could work |
| Green Hat | Alternatives, experiments, reframing, and new ideas |
| Blue Hat | Thinking process, sequence, scope, decision criteria, and next steps |
| Orchestrator | Route work to all six hats, compare outputs, expose blind spots, and synthesize the whole |

The **Blue Hat is not the Orchestrator** in this implementation. Blue is one of the six viewpoints. The Orchestrator sits outside the framework so it can compare all six outputs without collapsing them into a single preferred style.

## The elephant principle

The blind-men-and-elephant parable is a useful model for multi-agent work: one perspective can be locally valid and globally incomplete. A good orchestrator therefore seeks more than consensus. It looks for the *shape of the whole elephant* and for the *elephants in the room*—unstated assumptions, missing stakeholders, incentives, dependencies, ethical concerns, or second-order effects.

## Start in the browser

- [Open the JupyterLite lab](https://jltobias.github.io/JupyterLite-AI-Agents-and-Orchestrator-Six-Thinking-Hats/lite/lab/index.html)
- [Open Notebook 1 directly](https://jltobias.github.io/JupyterLite-AI-Agents-and-Orchestrator-Six-Thinking-Hats/lite/lab/index.html?path=01_six_hats_agents.ipynb)

No local Python installation is required for the JupyterLite labs.
