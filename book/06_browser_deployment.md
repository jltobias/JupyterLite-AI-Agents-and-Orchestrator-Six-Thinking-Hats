# Browser deployment with JupyterBook + JupyterLite

This repository deploys two complementary experiences from one GitHub Pages site.

## JupyterBook

JupyterBook turns the Markdown chapters and notebooks into a navigable learning site. The project uses the current MyST-based `myst.yml` configuration.

Build locally with:

```bash
jupyter book build --html
```

The static site is written to `_build/html`.

## JupyterLite

JupyterLite packages JupyterLab and a Python kernel that runs in the browser via WebAssembly/Pyodide. The notebooks and `six_hats_agents.py` module are copied into the Lite site:

```bash
jupyter lite build --contents notebooks --output-dir _build/html/lite
```

The result is one deployable directory:

```text
_build/html/
├── ... JupyterBook files ...
└── lite/
    ├── lab/
    └── ... JupyterLite assets ...
```

## GitHub Pages

`.github/workflows/pages.yml` builds both sites on pushes to `main` and uploads `_build/html` as the Pages artifact.

One repository setting is still required because workflows cannot safely assume Pages has been enabled:

1. Open **Settings → Pages**.
2. Set **Source** to **GitHub Actions**.
3. Re-run the Pages workflow if necessary.

Then the book and notebook links in the root README should resolve under:

`https://jltobias.github.io/JupyterLite-AI-Agents-and-Orchestrator-Six-Thinking-Hats/`

## Why this is easy to share

The learner needs only a modern web browser. The book explains concepts; JupyterLite provides editable notebooks next to the explanations; no local Python environment is required for the default labs.

## Upstream documentation

- JupyterBook publishing: https://jupyterbook.org/stable/get-started/publish/
- JupyterLite GitHub Pages deployment: https://jupyterlite.readthedocs.io/en/latest/quickstart/deploy.html
