# Introduction to MCP (Model Context Protocol)

A beginner-friendly introduction to MCP (Model Context Protocol).

## What is MCP?

MCP stands for Model Context Protocol. It is an open protocol that enables AI
models to securely interact with external tools, data sources, APIs, and
applications through a standardized interface.

MCP acts as a universal integration layer between AI systems and external
services, making tool integration and context sharing consistent and
interoperable across platforms.

## Why use MCP?

MCP simplifies how AI applications connect with external systems. Instead of
building custom integrations for every tool or API, developers can use a
standardized protocol for communication.

Benefits of MCP include:

- Standardized integration between AI models and tools
- Secure access to external resources and services
- Reusable and interoperable tool ecosystems
- Easier development of AI agents and assistants
- Consistent communication across platforms and applications

## Core MCP Concepts

MCP typically involves:

- **MCP Hosts** — Applications that use AI models
- **MCP Clients** — Components that communicate using MCP
- **MCP Servers** — Services that expose tools, resources, and prompts
- **Tools** — Functions AI models can execute
- **Resources** — External data sources available to models
- **Prompts** — Reusable prompt templates and workflows

## How MCP Works

1. An AI application connects to an MCP server.
2. The MCP server exposes available tools and resources.
3. The AI model discovers and invokes tools through the MCP interface.
4. Results are returned in a standardized format.
5. The AI application uses the returned context to generate responses or perform
   actions.

## Use Cases

- AI coding assistants
- RAG (Retrieval-Augmented Generation) systems
- AI agents with tool access
- Enterprise AI integrations
- Database and API connectivity
- Multi-tool AI workflows

## Learn More

- MCP architecture
- MCP clients and servers
- Tool integration
- Resources and prompts
- Building custom MCP servers
- Security and transport layers

## Repository layout (contributors)

**`source-material/`** — Optional local folder for raw instructor or author notes.
It is listed in `.gitignore`, so it may be absent in a fresh clone. Anything that
becomes learner-facing must be written in normal project paths (for example
`docs/`, `src/`) with original wording and structure, not copied from intake
files. For the full policy for humans and AI tools, see **`AGENTS.md`**.

Assistant-specific rules also live under **`.github/`**, **`.cursor/rules/`**,
and **`.claude/`** (next to root **`CLAUDE.md`** and **`skills.md`**).

## Local development ([uv](https://docs.astral.sh/uv/))

This repo uses **uv** for Python tooling. Install uv using the upstream
instructions for your OS, then:

### `uv init`

Creates a new project layout (for example `pyproject.toml` and related
defaults). Use this when you are **starting a brand-new Python project** from an
empty directory. **This repository already ships a `pyproject.toml`**, so you
normally **do not** run `uv init` here unless you are intentionally
re-scaffolding.

### `uv sync --all-groups --link-mode=copy`

Installs dependencies from the lockfile into the project environment and
includes **every optional dependency group** (for example dev or docs groups when
they exist in `pyproject.toml`). **`--link-mode=copy`** copies files into the
environment instead of hardlinking, which avoids issues on some **Windows** and
**network / shared** filesystems.

New project (empty directory):

```bash
uv init
```

This repository (install all groups, stable linking on Windows / shared disks):

```bash
uv sync --all-groups --link-mode=copy
```

After `uv sync`, use **`uv run …`** to execute Python tools and scripts with
that environment.
