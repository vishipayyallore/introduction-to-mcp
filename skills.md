# skills.md

Repository-level skill index for contributors and AI assistants.

## Core Skills

1. MCP server implementation with FastMCP (tools, resources, prompts, transports).
2. Zero-copy transformation workflow from instructor intake notes.
3. Demo-to-docs alignment (`src/demos/0N-name/` ↔ `docs/notes/` topic files and README tables).
4. Markdown quality and link integrity checks.
5. Python quality checks with ruff and compileall.
6. Transport configuration (stdio and Streamable HTTP).

## Guardrails

- Treat `source-material/` as an internal, read-only intake folder (often gitignored locally; not
  guaranteed in every clone).
- Do not copy source text verbatim into publish-facing documentation.
- Keep demo references accurate: URI templates, tool names, port numbers, and run commands must
  match the actual implementation.
- Default new demo content to unimplemented demo slots (05 onwards); do not modify existing demos
  without explicit instruction from Swamy.

## Policy vs runnable skills

Intake and zero-copy expectations are expressed in **repository instructions** (root `AGENTS.md`,
`CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules/`, `.claude/AGENTS.md`,
`.claude/rules/`) — not as a separate installable skill file. Treat this `skills.md` file as the
**canonical skill index**; `.claude/skills.md` extends it for Claude Code usage notes.
