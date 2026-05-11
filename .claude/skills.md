# skills.md — Claude Code Skill Index

Repository-level skill index for Claude Code agents working in this repo.
Extends the root `skills.md` with Claude-specific application notes. See
[`.claude/rules/README.md`](rules/README.md) for rule supplements (including
`source-material/` intake).

---

## Core Skills

1. **MCP server implementation** — write FastMCP servers with tools, resources, and prompts;
   configure stdio and Streamable HTTP transports; use `asyncio.to_thread` for blocking I/O.
2. **Zero-copy transformation** — adapt ideas from instructor intake notes into fully original
   documentation: new wording, new examples, new structure.
3. **Demo-to-docs alignment** — keep `src/demos/0N-name/README.md` and `docs/notes/` in sync
   with the actual implementation (tool names, resource URI templates, port numbers, run commands).
4. **Markdown quality and link integrity** — validate with `markdownlint-cli2` before finishing
   doc tasks.
5. **Python quality checks** — apply `ruff check` and `compileall` before completing any task.
6. **Demo progression discipline** — route new code to unimplemented demo slots (05 onwards);
   never modify existing completed demos without explicit approval.

---

## Guardrails

- **`source-material/` is internal, read-only intake** (often gitignored; not in every clone).
  Do not copy source text into publish-facing docs.
- **Do not surface internal process in learner docs.** Intake policy is agent/contributor
  guidance only.
- **Keep docs accurate:** tool names, resource URI templates, port numbers, and run commands
  must match the actual implementation in `server.py` and the DB helper files.
- **Default new additions to unimplemented demo slots** (05 onwards). Do not change existing
  demos without Swamy's explicit approval.

## Runnable skills vs repository instructions

There is **no** separate installable skill file under `.claude/`, `.cursor/`, or `.github/`
whose sole scope is `source-material/`. Zero-copy and intake expectations live in shared rules
and AGENTS files; this document and root `skills.md` describe how to apply those expectations
in practice.
