# Source material intake (`source-material/`)

## What this folder is

`source-material/` holds **internal, read-only** instructor intake: rough notes, transcripts, or
other raw references. It is **not** learner-facing curriculum and must not be copied into publish
paths as-is.

This repository lists `source-material/` in **`.gitignore`**, so clones may not include it; when
present locally, treat it as **private working notes** for authors and automation, not part of the
shipped tutorial surface.

## Required behavior

1. **Transform, do not transcribe** — Rebuild explanations with new structure, voice, and examples.
   Do not reuse wording, section order, or narration from intake files.
2. **No verbatim blocks** — No pasting from source-material into `docs/`, README, or formal
   `src/L{level}/S{session}/` paths.
3. **No citations of intake paths** — Do not link to or name `source-material/…` in anything
   learners or public readers see.
4. **Session placement** — Material inspired by intake belongs in **planned or new** sessions by
   default; do not add to **completed** sessions without explicit approval in the current task.

## Where the full policy lives

- Root **`AGENTS.md`** — agent checks, session bucketing, precedence.
- **`.github/copilot-instructions.md`** — GitHub Copilot copy of intake rules.
- **`.cursor/rules/01_educational-content-rules.mdc`** — Cursor rule pack (educational + intake).
- Root **`CLAUDE.md`** and **`.claude/AGENTS.md`** — Claude Code baseline and supplements.
