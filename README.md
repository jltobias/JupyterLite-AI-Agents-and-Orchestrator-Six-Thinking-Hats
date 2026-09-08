# JupyterLite AI Agents + Orchestrator: Six Thinking Hats

A browser-first learning project for exploring **AI agents**, **multi-agent orchestration**, and **Edward de Bono's Six Thinking Hats**. Six role-specialized agents examine one problem from different perspectives, while a seventh **Orchestrator** gathers their outputs, looks for blind spots, and constructs a whole-system view—the proverbial **elephant in the room**.

## Live learning

> GitHub Pages must be enabled with **Settings → Pages → Source: GitHub Actions** before these links become live.

- **JupyterBook:** https://jltobias.github.io/JupyterLite-AI-Agents-and-Orchestrator-Six-Thinking-Hats/
- **JupyterLite Lab:** https://jltobias.github.io/JupyterLite-AI-Agents-and-Orchestrator-Six-Thinking-Hats/lite/lab/index.html
- **Notebook 00 — Six Thinking Hats Foundations + Global Health:** https://jltobias.github.io/JupyterLite-AI-Agents-and-Orchestrator-Six-Thinking-Hats/lite/lab/index.html?path=00_six_thinking_hats_foundations.ipynb
- **Notebook 01 — Six Hat Agents:** https://jltobias.github.io/JupyterLite-AI-Agents-and-Orchestrator-Six-Thinking-Hats/lite/lab/index.html?path=01_six_hats_agents.ipynb
- **Notebook 02 — Orchestrator Lab:** https://jltobias.github.io/JupyterLite-AI-Agents-and-Orchestrator-Six-Thinking-Hats/lite/lab/index.html?path=02_orchestrator_lab.ipynb
- **Notebook 03 — Build Your Own Backend:** https://jltobias.github.io/JupyterLite-AI-Agents-and-Orchestrator-Six-Thinking-Hats/lite/lab/index.html?path=03_backend_adapter.ipynb

## What you will learn

1. The conceptual foundations of **Six Thinking Hats**, including parallel thinking and why hats are modes rather than personality types.
2. How the framework can be applied to complex global-health questions such as outbreak response, vaccine delivery, maternal health, malaria, antimicrobial resistance, and climate-health preparedness.
3. What makes an AI agent different from a single prompt.
4. How to represent the six hats as role-specialized agents.
5. Why the **Blue Hat agent** and the **Orchestrator** are related but distinct:
   - Blue Hat manages the *thinking process* from within the Six Hats framework.
   - The Orchestrator is the *multi-agent coordinator* that invokes all six agents, preserves their independent perspectives, detects disagreement and blind spots, and synthesizes the big picture.
6. How the story of the **blind men and the elephant** illustrates partial truth, perspective blindness, and the need for synthesis.
7. How to run the learning environment entirely in a browser with JupyterLite.
8. How to replace the included browser-safe teaching backend with a real LLM through a secure backend/proxy.

## Architecture

```text
                         ┌──────────────────────────────┐
                         │          Orchestrator         │
                         │ route • compare • synthesize │
                         │ find blind spots • next steps│
                         └──────────────┬───────────────┘
                                        │
          ┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
          │          │          │          │          │          │          │
       White       Red       Black      Yellow      Green       Blue
       facts     feelings     risks     benefits   creativity   process
```

Each Hat Agent receives the same problem plus shared context, but it has a different role prompt and output contract. The Orchestrator does **not** erase disagreement. Instead, it asks:

- What did each perspective notice?
- Which claims are facts, hypotheses, feelings, risks, benefits, alternatives, or process observations?
- Where do the perspectives reinforce or contradict one another?
- What information is missing?
- What assumptions, stakeholders, incentives, dependencies, ethical concerns, or second-order effects may be the **elephants in the room**?
- What should we investigate, decide, test, or sequence next?

### Fidelity note

In de Bono's original human-group method, participants generally use the **same hat at the same time** and move through hats in sequence—parallel thinking. This repository's six simultaneous/specialized Hat Agents are a **computational adaptation** intended to guarantee perspective coverage before orchestration, not a claim that people should be permanently assigned different hats.

## Browser-safe by design

The included notebooks use a deterministic `TeachingBackend`, so they run in JupyterLite without credentials or a server. This backend is intentionally transparent: it teaches the mechanics of agent roles, prompts, routing, structured outputs, and synthesis rather than pretending to be a generative model.

A `CallableBackend` adapter is also included. You can connect it to a real LLM later, but **do not place long-lived API keys in a public notebook or browser JavaScript**. Prefer a server-side proxy, short-lived credentials, or an authenticated service that keeps secrets off the client.

## Repository layout

```text
.
├── .github/workflows/pages.yml   # Build JupyterBook + JupyterLite and deploy Pages
├── book/                         # JupyterBook chapters
├── notebooks/                    # Browser-run JupyterLite labs
│   ├── assets/
│   │   └── six-thinking-hats.svg # Original color graphic used by Notebook 00
│   ├── 00_six_thinking_hats_foundations.ipynb
│   ├── six_hats_agents.py        # Reusable agents + orchestrator
│   ├── 01_six_hats_agents.ipynb
│   ├── 02_orchestrator_lab.ipynb
│   └── 03_backend_adapter.ipynb
├── myst.yml                      # JupyterBook 2 / MyST configuration
├── requirements.txt
└── README.md
```

## Local build (optional)

```bash
python -m pip install -r requirements.txt
jupyter book build --html
jupyter lite build --contents notebooks --output-dir _build/html/lite
python -m http.server 8000 --directory _build/html
```

Then open `http://localhost:8000/` for the book and `http://localhost:8000/lite/lab/index.html` for JupyterLite.

## References and attribution

The project is an educational implementation inspired by Edward de Bono's Six Thinking Hats method; it is not affiliated with or endorsed by the de Bono organization.

- de Bono, Edward. *Six Thinking Hats*. Little, Brown and Company, 1985; later Penguin editions are available. Official overview: https://www.debono.com/Books/six-thinking-hats
- Official Six Thinking Hats site, including guidance on parallel thinking: https://www.six-thinking-hats.com/
- Stikeleather, James, and Anthony J. Masys. “Global Health Security Innovation.” In *Global Health Security: Recognizing Vulnerabilities, Creating Opportunities*, Springer, 2020, pp. 387–425. https://doi.org/10.1007/978-3-030-23491-1_16
- Zhang, Xiao Chi, et al. “A Novel Approach to Debriefing Medical Simulations: The Six Thinking Hats.” *Cureus* 10(4), 2018: e2543. https://doi.org/10.7759/cureus.2543
- Lachman, Peter, ed. “Application of QI methods: Preparing your QI project.” *Handbook of Quality Improvement in Healthcare*, Oxford University Press, 2024. https://doi.org/10.1093/med/9780192866387.003.0017
- NHS Institute for Innovation and Improvement. *The Handbook of Quality and Service Improvement Tools*, section 7.2, “Six Thinking Hats.” https://www.england.nhs.uk/commissioning/wp-content/uploads/sites/44/2017/11/the_handbook_of_quality_and_service_improvement_tools_2010-2.pdf
- The **blind men and the elephant** is an old parable with versions in South Asian religious and literary traditions. A Buddhist version appears in *Udāna* 6.4; an English public-domain rendering is available via Project Gutenberg: https://www.gutenberg.org/files/74064/74064-h/74064-h.htm
- John Godfrey Saxe (1816–1887) popularized the parable in English verse as “The Blind Men and the Elephant.” A public-domain text appears in Project Gutenberg's *The Elson Readers, Book 5*: https://www.gutenberg.org/cache/epub/9106/pg9106-images.html#THE_BLIND_MEN_AND_THE_ELEPHANT

## License

No open-source license has been selected yet. Add a `LICENSE` file before inviting others to redistribute or modify the repository. Third-party concepts and cited works retain their respective rights; citations are provided for attribution and further reading.
