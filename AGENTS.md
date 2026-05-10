# AGENTS.md

Repository agent guidance for automation and code assistants.

## Default Agent Responsibilities

1. Preserve existing educational structure and learner flow.
2. Make minimal, targeted edits unless broader refactors are explicitly approved.
3. Validate docs and code quality before finishing work.

## Required Checks Before Completion

1. `ruff check src`
2. `python -m compileall -q src`
3. `npx --yes markdownlint-cli2 "README.md" "docs/**/*.md" ".github/**/*.md"`
4. `./scripts/docs-links.ps1` (Docker required)

## Source Intake Policy

- `source-material/` is an internal, read-only intake folder for instructor notes.
- Publish-facing docs must be transformative and original.
- Avoid copying wording, sequence, or examples directly from intake notes.

## `src/Working/` modification policy (Swamy-owned sandbox)

- **Do not** create, edit, move, rename, or delete files under `src/Working/` **unless Swamy explicitly asks** for that change in the current task (e.g. “update `src/Working/Module1/02_sample.py`” or “add a draft under Working”).
- You may still **read** `docs/RepositoryStructure.md` (section **src/Working/**) for routing context when advising on promotion into `src/L{level}/S{session}/`.
- Routine automation (formatting entire `src/`, mass refactors) must **exclude** or skip `src/Working/` unless the task scope includes it by name.

## Session Bucket Safety Policy

- Treat `docs/meetup/L1/meetup-sessions.md` table as the delivery-status signal for Level 1 meetup sessions.
- New curriculum content derived from `source-material/` or `src/Working/` must be bucketed into planned/new sessions by default.
- Do not add new learning content to already completed sessions unless the user gives explicit approval in the current task.
- If session status is unclear, pause and ask permission before placing content.
- **Topic → folder map (L1 from `S5` onward):** `docs/RepositoryStructure.md` (section **src/Working/**)

## Notes

- This file is repository-local and complements `.github/copilot-instructions.md` and `CLAUDE.md`.
- If guidance conflicts, follow this precedence: `docs/RepositoryStructure.md` (structure source of truth) → `.github/copilot-instructions.md` → `CLAUDE.md` → this file.
