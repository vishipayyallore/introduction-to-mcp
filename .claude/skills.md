# skills.md — Claude Code Skill Index

Repository-level skill index for Claude Code agents working in this repo.
Extends the root `skills.md` with Claude-specific application notes.

---

## Core Skills

1. **Educational content design** — structure 30-minute beginner Python sessions with clear
   objectives, concept explanations, worked examples, and practice files.
2. **Zero-copy transformation** — adapt ideas from instructor intake notes into fully original
   curriculum content: new wording, new examples, new pedagogical structure.
3. **Session-to-practice alignment** — keep `docs/sessions/L{level}/S{session}.md` in sync
   with `src/L{level}/S{session}/` practice files (names, numbering, learning outcomes).
4. **Markdown quality and link integrity** — validate headings, links, and formatting with
   `markdownlint-cli2` before finishing doc tasks.
5. **Python quality checks** — apply `ruff check` and `compileall` with pedagogy-aware lint
   policy (relax unused-variable warnings in educational demo files).
6. **Session-bucketing discipline** — route all new content to planned/new sessions; never
   inject into completed sessions without explicit approval.
7. **Working → Formal promotion** — follow the five-step promotion workflow when Swamy asks
   to move a file from `src/Working/` to `src/L{level}/S{session}/`.

---

## Guardrails

- **`source-material/` is internal, read-only intake** (often gitignored locally; not guaranteed in
  every clone). Do not copy source text — not even paraphrased structure — into publish-facing
  documentation. Transform every idea completely.
- **Do not surface internal process in curriculum docs.** Intake policy, zero-copy rules, and
  Working promotion steps are agent/contributor guidance only; omit them from session docs.
- **Keep references on formal curriculum paths** (`src/L{level}/S{session}/`), never on
  sandbox paths (`src/Working/`).
- **Default new additions to planned/new sessions.** Do not inject into completed sessions
  without Swamy's explicit approval in the current task message.
- **`src/Working/` is hands-off** unless Swamy explicitly names that path in the current task.
  Prefer formal `src/L{level}/S{session}/` and `docs/sessions/` for all curriculum work.

## Runnable skills vs repository instructions

There is **no** separate installable skill file under `.claude/`, `.cursor/`, or `.github/` whose
sole scope is `source-material/`. Zero-copy and intake expectations live in shared **rules and
AGENTS** files; this document and root **`skills.md`** describe how to apply those expectations in
practice.
