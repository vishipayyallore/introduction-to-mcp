# AGENTS.md — Claude-Specific Agent Guidance

Claude Code agent rules for this repository. This file adds Claude-specific detail and defers to
root `CLAUDE.md` and root `AGENTS.md` for baseline policy.

---

## Core Responsibilities

1. Preserve learner flow and existing session structure.
2. Make targeted edits; ask before broad or risky changes.
3. Run all quality checks before marking a task complete.

---

## Source Intake Policy

`source-material/` is an internal, read-only folder for instructor notes and raw session transcripts.
Agent output must be **transformative**: rewrite every concept in fresh language, with new examples
and original pedagogical structure.

Rules:

- Do not copy wording, sequence, or narration from intake notes into any publish-facing doc.
- Do not reference `source-material/` paths in session docs, READMEs, or curriculum files.
- Extract only the core concept or student misconception, then explain it entirely from scratch.
- Internal policy from source-material handling must not appear in user-visible curriculum content.

---

## Session Bucket Safety

New content adapted from `source-material/` — or from any external reference — must be placed in a
planned or new session by default. Do not add material to a completed session without Swamy's
explicit instruction in the current task message.

When the target session is unclear, consult `docs/meetup/L1/meetup-sessions.md` and ask for
confirmation before writing any content.

---

## Precedence Order

When instructions conflict, **first** follow the **Notes → precedence** chain in root **`AGENTS.md`**
(which names `docs/RepositoryStructure.md` when present, then `.github/copilot-instructions.md`,
then `CLAUDE.md`, then root `AGENTS.md`).

For gaps not covered there, use this Claude-specific tie-break (highest wins):

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
