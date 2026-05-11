# Claude Code Instructions — Introduction to MCP

**Project:** Introduction to MCP (Model Context Protocol)
**Purpose:** Hands-on MCP learning demos, conceptual notes, and reference documentation.

Read this file together with root **`AGENTS.md`** (automation checks, intake policy, and
precedence). For Claude-specific supplements, see **`.claude/AGENTS.md`** and **`.claude/rules/`**.

---

## 🚨 Critical Rules

1. **Zero-Copy Policy** — All educational content must be original and transformative. Never copy
   verbatim from transcripts, books, or third-party material.
2. **Preserve existing structure** — Read the full file before editing. Make minimal, targeted
   changes.
3. **Do not corrupt content** — If a change feels broad or risky, ask first.
4. **Source-material is read-only** — `source-material/` is internal instructor intake. Never
   reference its paths in learner-facing docs. Transform ideas; never copy text.

---

## 🔒 Internal Content Intake Policy

- Borrow ideas and teaching patterns, not exact text, section order, or narration.
- Treat `source-material/` as internal, read-only instructor notes; rewrite explanations with
  original structure and wording.
- When in doubt, ask before placing or changing content.
- This policy is internal process guidance and must not appear in learner-facing docs.

---

## 📁 Repository Structure (Quick Reference)

```text
introduction-to-mcp/
├── docs/
│   ├── images/          # screenshots and diagrams
│   ├── notes/           # conceptual MCP notes (setup + 01–08)
│   └── references/      # command references (uv-commands.md, python_commands.md)
├── src/
│   ├── demos/           # hands-on demo servers and clients
│   │   ├── 01-calculator/
│   │   ├── 02-typed-calculator/
│   │   ├── 03-leave-manager/
│   │   ├── 04-project-tracker/
│   │   └── (05–10 planned)
│   └── shared/          # reusable helpers shared across demos
├── tools/psscripts/     # CI scripts
├── .claude/             # Claude Code supplements (AGENTS, skills, rules/)
├── .cursor/rules/       # Cursor AI rule files
├── .github/             # Copilot instructions and workflows
├── AGENTS.md            # Agent guidance
├── CLAUDE.md            # This file
└── skills.md            # Repo skill index
```

---

## 🗂️ Demo Structure (`src/demos/`)

Each demo is self-contained:

```text
0N-demo-name/
├── server.py            # FastMCP server
├── client.py            # HTTP/stdio client
├── [helpers].py         # Pydantic models or DB helpers (demo-specific)
├── settings.py          # Config loader
├── config/settings.json # Port, transport, server name
└── README.md            # Demo docs
```

Demo numbering starts at `01-`. No `00-` prefix ever.

Ports are allocated sequentially: `01→8000`, `02→8001`, `03→8002`, `04→8003`, and so on.

---

## 💻 Code Standards

- All demo files must run without errors (`ruff check src`, `python -m compileall -q src`).
- Type annotations and tool docstrings must be accurate — the docstring is what the model reads.
- Keep `server.py` clean and focused on FastMCP declarations; move DB/business logic to helpers.

---

## 🔗 Related Files

- **Cursor rules:** `.cursor/rules/`
- **Claude supplements:** `.claude/AGENTS.md`, `.claude/skills.md`, `.claude/rules/`
- **Copilot instructions:** `.github/copilot-instructions.md`
