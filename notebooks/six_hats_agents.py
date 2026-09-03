"""Six Thinking Hats agents and a browser-safe teaching orchestrator.

This module intentionally depends only on the Python standard library so it can run
inside JupyterLite/Pyodide.  Replace TeachingBackend with CallableBackend when you
have a secure way to call a real language model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, Mapping, Protocol
import re
import textwrap


class Backend(Protocol):
    """Minimal model/backend interface used by every hat agent."""

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        ...


@dataclass(frozen=True)
class HatConfig:
    name: str
    label: str
    purpose: str
    system_prompt: str


@dataclass
class Perspective:
    hat: str
    label: str
    purpose: str
    response: str


COMMON_RULES = """
Shared rules:
- Stay inside your assigned thinking mode.
- Do not make the final decision for the group.
- Separate observations from assumptions and hypotheses.
- Do not invent facts or citations.
- Be concise, specific, and decision-useful.
- End with one question the Orchestrator should carry forward.
""".strip()


HATS: Dict[str, HatConfig] = {
    "white": HatConfig(
        "white",
        "White Hat — Facts",
        "Known information, evidence, unknowns, and information needs.",
        """You are the White Hat agent. Focus on information: what is known, what is claimed, what is missing, and what evidence would reduce uncertainty. Explicitly distinguish facts supplied by the user from assumptions. Identify data-quality and provenance questions.""",
    ),
    "red": HatConfig(
        "red",
        "Red Hat — Feelings",
        "Intuition, emotions, stakeholder reactions, and instinctive concerns.",
        """You are the Red Hat agent. Surface intuitive reactions, emotions, unease, enthusiasm, and possible stakeholder sentiment. Feelings do not need logical proof, but label them as feelings or hypotheses rather than facts. Include more than one stakeholder where relevant.""",
    ),
    "black": HatConfig(
        "black",
        "Black Hat — Risks",
        "Failure modes, constraints, cautions, and reasons a plan might not work.",
        """You are the Black Hat agent. Stress-test the idea. Identify concrete failure modes, constraints, dependencies, unintended consequences, and conditions under which the proposal could fail. Connect risks to mechanisms; do not be negative merely for balance.""",
    ),
    "yellow": HatConfig(
        "yellow",
        "Yellow Hat — Benefits",
        "Value, opportunities, strengths, and reasons an idea could work.",
        """You are the Yellow Hat agent. Look for plausible benefits, strengths, value, opportunities, and favorable conditions. Explain why benefits could occur and how they might be measured. Do not turn optimism into unsupported certainty.""",
    ),
    "green": HatConfig(
        "green",
        "Green Hat — Creativity",
        "Alternatives, reframing, experiments, combinations, and new possibilities.",
        """You are the Green Hat agent. Generate alternatives, reframings, experiments, combinations, and novel options. Challenge hidden constraints. Produce several possibilities before favoring any one. Turn major objections into design prompts.""",
    ),
    "blue": HatConfig(
        "blue",
        "Blue Hat — Process",
        "Thinking process, scope, sequence, criteria, and what should happen next.",
        """You are the Blue Hat agent. Think about the thinking process. Clarify the decision question, scope, sequence, decision criteria, and what additional thinking is required. Identify which hat should be revisited and why. You manage process from within the Six Hats framework; you are not the software Orchestrator.""",
    ),
}


class HatAgent:
    """A role-specialized agent that delegates completion to a backend."""

    def __init__(self, config: HatConfig, backend: Backend):
        self.config = config
        self.backend = backend

    def build_prompts(self, problem: str, context: str = "") -> tuple[str, str]:
        system = f"{self.config.system_prompt}\n\n{COMMON_RULES}"
        user = textwrap.dedent(
            f"""
            Problem or decision:
            {problem.strip()}

            Shared context:
            {context.strip() or '(No additional context supplied.)'}

            Respond from the {self.config.label} perspective.
            """
        ).strip()
        return system, user

    def analyze(self, problem: str, context: str = "") -> Perspective:
        system, user = self.build_prompts(problem, context)
        return Perspective(
            hat=self.config.name,
            label=self.config.label,
            purpose=self.config.purpose,
            response=self.backend.complete(system, user),
        )


class CallableBackend:
    """Adapter for a real model function: fn(system_prompt, user_prompt) -> str."""

    def __init__(self, fn: Callable[[str, str], str]):
        self.fn = fn

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        return self.fn(system_prompt, user_prompt)


def _extract_problem(user_prompt: str) -> str:
    match = re.search(r"Problem or decision:\s*(.*?)\n\nShared context:", user_prompt, re.S)
    return (match.group(1).strip() if match else user_prompt.strip())


def _extract_context(user_prompt: str) -> str:
    match = re.search(r"Shared context:\s*(.*?)\n\nRespond from", user_prompt, re.S)
    return (match.group(1).strip() if match else "")


def _hat_from_system(system_prompt: str) -> str:
    lower = system_prompt.lower()
    for name in HATS:
        if f"{name} hat" in lower:
            return name
    return "unknown"


class TeachingBackend:
    """Deterministic backend that teaches agent mechanics without pretending to be an LLM."""

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        hat = _hat_from_system(system_prompt)
        problem = _extract_problem(user_prompt)
        context = _extract_context(user_prompt)
        context_supplied = bool(context and "No additional context" not in context)
        short_problem = " ".join(problem.split())

        if hat == "white":
            bullets = [
                f"**Supplied decision:** {short_problem}",
                "**Known from the prompt:** the decision statement itself; any additional claims should be treated as unverified unless supported in the shared context.",
                (f"**Context available:** {context}" if context_supplied else "**Context available:** none beyond the decision statement."),
                "**Information gaps:** objectives, stakeholders, baseline performance, constraints, costs, timing, success measures, and evidence sources.",
                "**Evidence to seek:** authoritative data, comparable cases, user/stakeholder input, operational constraints, and measurable acceptance criteria.",
                "**Carry-forward question:** Which missing fact would most change the decision?",
            ]
        elif hat == "red":
            bullets = [
                "**Immediate intuition:** the proposal may create both curiosity and uncertainty because people often react to change before they can articulate a formal argument.",
                "**Possible positive feelings:** excitement, relief, ownership, or confidence if the change solves a visible pain point.",
                "**Possible negative feelings:** anxiety, loss of control, skepticism, fatigue, or fear of hidden consequences.",
                "**Stakeholder hypothesis:** people closest to implementation may feel differently from sponsors or beneficiaries; these are hypotheses to validate, not facts.",
                "**Carry-forward question:** Whose emotional reaction could determine adoption even if the technical case is strong?",
            ]
        elif hat == "black":
            bullets = [
                "**Failure mode 1:** the problem may be framed too narrowly, causing the solution to optimize one metric while shifting costs elsewhere.",
                "**Failure mode 2:** missing stakeholders, dependencies, permissions, budget, skills, or maintenance work could block implementation.",
                "**Failure mode 3:** early success may not generalize if the pilot context differs from real operating conditions.",
                "**Failure mode 4:** weak evidence or unclear accountability can turn assumptions into commitments prematurely.",
                "**Safeguard:** define stop/go criteria, owners, dependencies, and a small reversible test before scaling.",
                "**Carry-forward question:** What is the most damaging plausible failure that a small pilot should test first?",
            ]
        elif hat == "yellow":
            bullets = [
                "**Potential value:** a well-designed change could improve outcomes, speed, consistency, learning, or stakeholder experience.",
                "**Strategic upside:** the work may create reusable capabilities or knowledge beyond the immediate decision.",
                "**Operational upside:** explicit roles and decision criteria can reduce rework and make trade-offs visible.",
                "**Learning value:** even a limited pilot can produce evidence that improves later choices.",
                "**Measure the benefit:** choose a small set of before/after indicators tied to the stated objective.",
                "**Carry-forward question:** Which benefit would justify proceeding even if some secondary benefits do not materialize?",
            ]
        elif hat == "green":
            bullets = [
                "**Alternative 1 — Pilot:** test the idea with one bounded use case before a broad commitment.",
                "**Alternative 2 — Compare:** run the proposed approach beside the current approach and measure differences.",
                "**Alternative 3 — Reframe:** ask what underlying need the proposal addresses, then generate at least two non-obvious ways to meet that need.",
                "**Alternative 4 — Hybrid:** combine the strongest part of the new idea with the safest part of the existing process.",
                "**Creative constraint:** design an option that is reversible, low-cost, and informative even if it fails.",
                "**Carry-forward question:** What option becomes possible if the biggest assumed constraint is relaxed?",
            ]
        elif hat == "blue":
            bullets = [
                f"**Decision focus:** clarify exactly what must be decided about: {short_problem}",
                "**Suggested sequence:** White → Red → Yellow → Black → Green → Blue, then orchestration and targeted follow-up.",
                "**Decision criteria:** evidence quality, stakeholder impact, value, risk, reversibility, feasibility, and learning potential.",
                "**Process check:** separate discovery from commitment; do not treat the first synthesis as the final answer.",
                "**Revisit trigger:** return to White after major Green alternatives or Black risks introduce new factual questions.",
                "**Carry-forward question:** What decision can responsibly be made now, and what must remain provisional?",
            ]
        else:
            bullets = ["TeachingBackend could not determine the requested hat."]

        return "\n".join(f"- {item}" for item in bullets)


class SixHatsOrchestrator:
    """Coordinates six hat agents and constructs a transparent whole-elephant synthesis."""

    def __init__(self, backend: Backend | None = None, hat_order: Iterable[str] | None = None):
        self.backend = backend or TeachingBackend()
        self.hat_order = list(hat_order or ["white", "red", "black", "yellow", "green", "blue"])
        self.agents = {name: HatAgent(HATS[name], self.backend) for name in self.hat_order}

    def fan_out(self, problem: str, context: str = "") -> Dict[str, Perspective]:
        return {name: agent.analyze(problem, context) for name, agent in self.agents.items()}

    def synthesize(self, problem: str, perspectives: Mapping[str, Perspective]) -> str:
        # This deterministic synthesis is intentionally inspectable.  A production
        # version can pass the same perspective bundle to a model backend.
        lines = [
            "# Orchestrator Synthesis",
            "",
            f"**Decision/problem:** {problem.strip()}",
            "",
            "## What each perspective contributes",
        ]
        for name in self.hat_order:
            p = perspectives[name]
            first_line = next((ln for ln in p.response.splitlines() if ln.strip()), "(no response)")
            first_line = re.sub(r"^[-*]\s*", "", first_line)
            lines.append(f"- **{p.label}:** {first_line}")

        lines += [
            "",
            "## Cross-hat tensions to examine",
            "- Benefits may depend on assumptions that the White Hat has not yet verified.",
            "- Stakeholder enthusiasm or resistance may change feasibility even when the technical case looks strong.",
            "- Risk controls can reduce downside but may also reduce speed, simplicity, or upside.",
            "- Green alternatives may change the facts that White needs and the risks that Black should test.",
            "",
            "## Information gaps",
            "- Clarify objectives, stakeholders, constraints, baseline conditions, success measures, and evidence quality.",
            "- Identify which unknown would materially change the decision rather than collecting data indiscriminately.",
            "",
            "## Elephants in the room",
            "- Are all six hats inheriting the same flawed problem framing?",
            "- Who has power to approve, block, implement, or bear the consequences but is absent from the analysis?",
            "- What incentives could make stated goals differ from actual behavior?",
            "- What maintenance, governance, privacy, equity, security, ethical, or second-order effects are easy to omit?",
            "- What happens after the initial success period—who owns the system and how is failure detected?",
            "",
            "## Whole-elephant view",
            "Treat the six outputs as partial observations, not votes. Preserve the strongest evidence, the most consequential risk, the clearest value proposition, the most informative stakeholder reaction, the best alternative, and the Blue Hat's process guidance in one shared decision model.",
            "",
            "## Recommended next move",
            "Run a small, reversible learning step with explicit success/failure criteria. Use its evidence to revisit the White and Black Hats, then ask the Orchestrator to revise the synthesis rather than merely append new text.",
        ]
        return "\n".join(lines)

    def run(self, problem: str, context: str = "") -> Dict[str, object]:
        perspectives = self.fan_out(problem, context)
        synthesis = self.synthesize(problem, perspectives)
        return {"problem": problem, "context": context, "perspectives": perspectives, "synthesis": synthesis}


def print_perspectives(perspectives: Mapping[str, Perspective]) -> None:
    """Notebook-friendly plain-text renderer."""
    for p in perspectives.values():
        print("=" * 80)
        print(p.label)
        print(p.purpose)
        print("-" * 80)
        print(p.response)
        print()


def build_llm_synthesis_prompt(problem: str, perspectives: Mapping[str, Perspective]) -> tuple[str, str]:
    """Create prompts for replacing deterministic synthesis with a real model."""
    system = textwrap.dedent(
        """
        You are a multi-agent Orchestrator. Six specialized Six Thinking Hats agents
        have independently analyzed the same problem. Synthesize without erasing
        disagreement. Distinguish facts, feelings/hypotheses, risks, benefits,
        alternatives, and process observations. Explicitly identify information gaps,
        cross-hat tensions, shared assumptions, and 'elephants in the room' such as
        missing stakeholders, incentives, dependencies, ethics, governance, or
        second-order effects. Do not treat majority agreement as proof.
        """
    ).strip()
    bundle = "\n\n".join(
        f"## {p.label}\n{p.response}" for p in perspectives.values()
    )
    user = f"Problem:\n{problem.strip()}\n\nAgent perspectives:\n\n{bundle}\n\nProduce a decision-oriented synthesis and next steps."
    return system, user