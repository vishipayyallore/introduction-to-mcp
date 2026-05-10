# skills.md

Repository-level skill index for contributors and AI assistants.

## Core Skills

1. Educational content design for beginner Python (30-minute session blocks).
2. Zero-copy transformation workflow from instructor intake notes.
3. Session-to-practice alignment (`docs/sessions/L{level}/S{session}.md` <-> `src/L{level}/S{session}/`).
4. Markdown quality and link integrity checks.
5. Python quality checks with pedagogy-aware lint policy.
6. Session-bucketing discipline for new content (planned/new sessions first).

## Guardrails

- Treat `source-material/` as an internal, read-only intake folder.
- Do not copy source text verbatim into publish-facing documentation.
- Keep references on formal curriculum paths, not sandbox paths.
- Default new additions to planned/new sessions; do not inject into completed sessions without explicit user permission.
- **`src/Working/` is hands-off:** do not modify anything under `src/Working/` unless Swamy explicitly requests that path or folder in the current task; prefer formal `src/L{level}/S{session}/` and `docs/sessions/` for changes.
