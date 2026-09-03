# Build the six agents

Open `notebooks/six_hats_agents.py` alongside the labs. The implementation uses three layers.

## 1. Hat configuration

Each hat has a name, purpose, and system prompt. The prompt contains role-specific instructions plus shared rules such as:

- stay within the assigned perspective;
- distinguish evidence from inference;
- do not make the final decision;
- return a concise, inspectable response.

## 2. HatAgent

`HatAgent` is deliberately small. It receives a backend and a hat configuration, constructs the prompt, and asks the backend to complete it.

This is a useful architectural boundary: the **agent role does not care which model provider is behind the backend**.

## 3. Backend abstraction

The repository includes two backends:

- `TeachingBackend` — deterministic, browser-safe, and transparent. It produces structured teaching output without network calls.
- `CallableBackend` — wraps any Python callable with the signature `(system_prompt, user_prompt) -> str`.

That means the six agents can be learned in JupyterLite today and connected to an LLM later.

## Why not put an API key in JupyterLite?

JupyterLite runs in the user's browser. Any long-lived secret placed in the notebook, JavaScript, local storage, or network request can be exposed to the person using that browser and may also be leaked if the notebook is shared.

For real model calls, prefer:

```text
JupyterLite browser
      |
      | authenticated request (no long-lived provider key)
      v
Your small server / gateway
      |
      | secret stored server-side
      v
LLM provider
```

This keeps the notebook shareable while protecting credentials.

## Prompt design exercise

When you modify a hat prompt, ask:

- What information is this role uniquely responsible for?
- What should it *not* decide?
- What output structure will make orchestration easier?
- How can the prompt reduce hallucination or role drift?
- What evidence should be preserved for traceability?
