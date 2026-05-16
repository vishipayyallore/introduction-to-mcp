# AGENTS.md

Repository agent guidance for automation and code assistants.

## Naming and Numbering Conventions

- Demo folders use a two-digit prefix: `01-calculator/`, `02-typed-calculator/`.
- Sequential files use a two-digit prefix: `01_name.py`, `02_name.py`.
- **Numbers must start at `01`, never `00`.** Files and folders prefixed `00_` or `00-` are forbidden.
- Support folders with no natural sequence (e.g., `setup/`, `references/`, `shared/`) carry no
  numeric prefix.

## Default Agent Responsibilities

1. Preserve the existing demo progression and learner flow.
2. Make minimal, targeted edits unless broader refactors are explicitly approved.
3. Validate docs and code quality before finishing work.

## Required Checks Before Completion

1. `ruff check src tests`
2. `python -m compileall -q src`
3. `uv run pytest tests -q` (after `uv sync --all-groups` or equivalent so `pytest` is available)
4. `npx --yes markdownlint-cli2 "README.md" "docs/**/*.md" ".github/**/*.md"`
5. `./tools/psscripts/docs-links.ps1` (Docker required)

## Source Intake Policy

- `source-material/` is an internal, read-only intake folder for instructor notes. It is listed in
  `.gitignore`, so it may exist only on a maintainer's machine; it is not assumed present in every
  clone.
- Publish-facing docs must be transformative and original.
- Avoid copying wording, sequence, or examples directly from intake notes.
- Do not reference `source-material/` paths in any learner-facing document.

### Agent model (no dedicated "source-material agent")

There is **no** separate executable agent or skill whose only job is `source-material/`. Intake
rules apply to **every** assistant and automation run in this repo (root `AGENTS.md`, `.claude/`,
`.cursor/rules/`, `.github/copilot-instructions.md`).

## Notes

- This file is repository-local and complements `.github/copilot-instructions.md`, `CLAUDE.md`,
  and `.claude/` (for example `.claude/AGENTS.md`, `.claude/skills.md`, `.claude/rules/`).
- If guidance conflicts, follow this precedence: `.github/copilot-instructions.md` → `CLAUDE.md`
  → this file.
