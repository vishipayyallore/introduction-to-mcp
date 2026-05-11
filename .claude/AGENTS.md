# AGENTS.md — Claude-Specific Agent Guidance

Claude Code agent rules for this repository. This file adds Claude-specific detail and defers to
root `CLAUDE.md` and root `AGENTS.md` for baseline policy.

---

## Naming and Numbering Conventions

- Demo folders use a two-digit prefix starting at `01`: `01-calculator/`, `02-typed-calculator/`.
- Sequential files use `01_name.py`, `02_name.py`, …
- **`00_` and `00-` prefixes are forbidden** for all files and folders, no exceptions.
- Unnumbered support folders (e.g., `setup/`, `references/`, `shared/`) carry no numeric prefix.

---

## Core Responsibilities

1. Preserve learner flow and the existing demo progression.
2. Make targeted edits; ask before broad or risky changes.
3. Run all quality checks before marking a task complete.

---

## Source Intake Policy

`source-material/` is an internal, read-only folder for instructor notes and raw session
transcripts. Agent output must be **transformative**: rewrite every concept in fresh language,
with new examples and original structure.

Rules:

- Do not copy wording, sequence, or narration from intake notes into any publish-facing doc.
- Do not reference `source-material/` paths in READMEs, notes, or demo files.
- Extract only the core concept or teaching insight, then explain it entirely from scratch.
- Internal policy must not appear in user-visible content.

---

## Precedence Order

When instructions conflict, apply this chain (highest wins):

1. Explicit instruction in the current user message.
2. Root `CLAUDE.md`.
3. Root `AGENTS.md`.
4. This file (`.claude/AGENTS.md`).
5. `.claude/rules/*.md` (supplements such as [`rules/source-material-intake.md`](rules/source-material-intake.md)).
6. `.cursor/rules/` rule files.
7. `.github/copilot-instructions.md`.
8. `skills.md` (root) and `.claude/skills.md`.
9. Model defaults.

### No dedicated source-material agent

Intake policy is **not** a separate agent or MCP server in this repo. All Claude Code runs inherit
the same **source-material** rules documented here and in root **`AGENTS.md`**.

---

## Required Checks

Before marking any task complete:

- `ruff check src`
- `python -m compileall -q src`
- `npx --yes markdownlint-cli2 "README.md" "docs/**/*.md" ".github/**/*.md"`
- `./tools/psscripts/docs-links.ps1` (Docker required)
