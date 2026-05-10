# GitHub Copilot Instructions — Python Fundamentals

**Project:** Python Fundamentals Curriculum (Swamy's Tech Skills Academy)
**Purpose:** Guide Copilot for educational content development, session documentation, and practice code.

---

## Repository Overview

This repo contains a beginner Python curriculum structured in levels (L1, L2, …) and sessions (S1–S9, etc.).
Formal curriculum lives at `src/L{level}/S{session}/` and `docs/sessions/L{level}/`.
Sandbox drafts live in `src/Working/` — do not touch without explicit instruction from Swamy.

---

## Content Rules

### Core Principles

- Make minimal, targeted changes. Read the full file before editing.
- If a change feels broad or risky, pause and ask.
- Do not restructure, rename sections, or reorder content beyond the explicit task scope.

### Zero-Copy Requirement

All educational content must be original and transformative. Never reproduce verbatim text
from transcripts, books, or third-party materials. When adapting ideas from reference material,
restructure explanations with fresh wording, new examples, and an original pedagogical flow.
Paraphrase that preserves sentence structure still fails this requirement.

### Session Placement

Route new content to planned or new sessions by default.
Do not inject into completed sessions without Swamy's explicit approval in the current task message.

---

## Source Material Intake Policy

`source-material/` is an **internal, read-only** intake folder for instructor notes and raw session
transcripts. Its contents are strictly off-limits for direct use in publish-facing docs.

**When working with source-material, you must:**

- Borrow only the core concept or student misconception being addressed.
- Rewrite every explanation in fresh language with original structure, examples, and narration.
- Never preserve the original wording, section order, or narration flow.
- Never reference or link to `source-material/` paths in session docs or any user-visible content.

**Session Bucketing from source-material:**
New content derived from source-material must be routed to planned or new sessions first.
Do not add to completed sessions without Swamy's explicit go-ahead in the current task message.

**Git / clones:** `source-material/` is listed in `.gitignore`. Treat it as optional local intake;
do not assume every clone contains it.

### No dedicated “source-material agent”

GitHub Copilot does not use a separate agent or skill scoped only to `source-material/`. The intake
rules above apply to **every** Copilot-assisted edit in this repository.

---

## `src/Working/` Sandbox Policy

`src/Working/` is Swamy's personal sandbox. Do not create, edit, move, rename, or delete any
file there unless Swamy explicitly names that path in the current request.

Formal curriculum edits go to `src/L{level}/S{session}/` and `docs/sessions/L{level}/`.

---

## Practice Code Standards

- All files in `src/L{level}/S{session}/` must run without errors.
- Use the `main` / `HELP_TEXT` / `raise SystemExit(main(sys.argv))` template.
- Name files sequentially: `01_name.py`, `02_name.py`, …
- Include a file-header comment: `# Filename: src/L1/S2/01_variables.py`

---

## Quality Checklist

Before completing any task:

- `ruff check src`
- `python -m compileall -q src`
- `npx --yes markdownlint-cli2 "README.md" "docs/**/*.md" ".github/**/*.md"`
- `./scripts/docs-links.ps1` (Docker required)
