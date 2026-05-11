# GitHub Copilot Instructions — Introduction to MCP

**Project:** Introduction to MCP (Model Context Protocol)
**Purpose:** Guide Copilot for demo development, conceptual note authoring, and reference
documentation.

---

## Repository Overview

This repo contains hands-on MCP learning demos (`src/demos/`) and conceptual notes
(`docs/notes/`). Demo servers use FastMCP with SQLite or in-memory state and support both stdio
and Streamable HTTP transports. Documentation lives in `docs/notes/` (topics 01–08 plus setup)
and `docs/references/`.

Demo numbering starts at `01-`. No `00-` prefix ever. Ports are allocated sequentially:
`01→8000`, `02→8001`, `03→8002`, `04→8003`, and so on.

---

## Content Rules

### Core Principles

- Make minimal, targeted changes. Read the full file before editing.
- If a change feels broad or risky, pause and ask.
- Do not restructure, rename sections, or reorder content beyond the explicit task scope.

### Zero-Copy Requirement

All educational content must be original and transformative. Never reproduce verbatim text from
transcripts, books, or third-party materials. When adapting ideas from reference material,
restructure explanations with fresh wording, new examples, and an original pedagogical flow.
Paraphrase that preserves sentence structure still fails this requirement.

### Demo Accuracy

Docs must match the implementation. Tool names, resource URI templates, port numbers, and run
commands in `README.md` and `docs/notes/` must reflect what is actually in `server.py`,
`*_db.py`, and `config/settings.json`.

---

## Source Material Intake Policy

`source-material/` is an **internal, read-only** intake folder for instructor notes and raw
session transcripts. Its contents are off-limits for direct use in publish-facing docs.

**When working with source-material, you must:**

- Rewrite in fresh structure and voice; never reuse wording, section order, or narration.
- Never reference or link `source-material/` paths in docs or user-visible content.

**Git / clones:** `source-material/` is listed in `.gitignore`. Treat it as optional local
intake; do not assume every clone contains it.

### No dedicated source-material agent

GitHub Copilot does not use a separate agent or skill scoped only to `source-material/`. The
intake rules above apply to **every** Copilot-assisted edit in this repository.

---

## Practice Code Standards

- All files in `src/demos/` must run without errors.
- Type annotations on tool parameters and return types must be correct.
- Tool docstrings must be precise — the model reads them to decide when to call the tool.
- Name files sequentially: `01_name.py`, `02_name.py`, …
- **Numbers start at `01_`, never `00_`.** Zero-prefixed names are forbidden.

---

## Quality Checklist

Before completing any task:

- `ruff check src`
- `python -m compileall -q src`
- `npx --yes markdownlint-cli2 "README.md" "docs/**/*.md" ".github/**/*.md"`
- `./tools/psscripts/docs-links.ps1` (Docker required)
