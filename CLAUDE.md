# Claude Code Instructions — Python Fundamentals

**Project:** Python Fundamentals Curriculum (Swamy's Tech Skills Academy)
**Purpose:** Educational content development, session documentation, and practice code.

---

## 🚨 Critical Rules

1. **Zero-Copy Policy** — All educational content must be original and transformative. Never copy verbatim from transcripts, books, or third-party material. See `.cursor/rules/01_educational-content-rules.mdc`.
2. **Preserve existing structure** — Read the full file before editing. Make minimal, targeted changes.
3. **Do not corrupt content** — If a change feels broad or risky, ask first.
4. **Session-bucketing safety** — New content should go to planned/new sessions by default. Do not add new material to completed sessions without explicit user approval.
5. **`src/Working/` hands-off** — Do not add, edit, move, rename, or delete files under `src/Working/` unless **Swamy explicitly asks** for that Working change in the current message. For Working layout and promotion expectations, read **`docs/RepositoryStructure.md`** (section **src/Working/**); do all curriculum edits in `src/L{level}/S{session}/` and `docs/` unless Working is in scope by name.

## 🔒 Internal Content Intake Policy (Source Notes + Working)

- Borrow ideas and misconceptions, not exact text, section order, or narration.
- Treat `source-material/` as internal, read-only instructor notes; rewrite explanations with original structure and wording.
- Promote `src/Working/` examples only after cleanup, renaming, and fit-check against session outcomes — and only when Swamy has asked you to touch or promote those Working files.
- Keep publish-facing session references on formal paths (`src/L{level}/S{session}/`) and never on sandbox paths.
- When in doubt about target placement, use the meetup status table in `docs/meetup/L1/meetup-sessions.md` and ask for permission before touching completed sessions.
- Run normal quality checks on imported ideas: clarity, technical accuracy, and beginner pedagogy.
- This policy is internal process guidance and should not appear as a process block in publish-facing curriculum docs.

---

## 📁 Repository Structure (Quick Reference)

Full structure: `docs/RepositoryStructure.md` (single source of truth).

```text
python-fundamentals/
├── docs/
│   ├── 01_Python-Fundamentals-MasterPlan.md   # 18-level course roadmap
│   ├── RepositoryStructure.md                 # Authoritative structure doc
│   └── sessions/
│       ├── L1/   # Noob → Nerd (S1–S9, S5, S10, _Plan.md)
│       └── L2/   # Nerd → Novice
├── src/
│   ├── L1/       # Formal practice files: src/L1/S1/01_name.py
│   ├── L2/
│   └── Working/  # Sandbox — see docs/RepositoryStructure.md (src/Working/)
│       ├── Module1/   # Foundational drafts → L1/S1 or S2
│       ├── S5/ … S10/  # Staging → matching L1 folders
├── .cursor/rules/          # Cursor AI rule files
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/
└── CLAUDE.md               # This file
```

---

## 🗂️ `src/Working/` — Sandbox Staging Area

`src/Working/` holds **informal drafts**: `Module1/` for sessions 1–2 style samples, and **`S5/` through `S10/`** as staging lanes that match formal `src/L1/…` folders. See **`docs/RepositoryStructure.md`** (section **src/Working/**) for layout and promotion expectations. Promote into `src/L{level}/S{session}/` when ready.

### Working vs Formal

| `src/Working/` staging | `src/L{level}/S{session}/` |
|---|---|
| Informal, exploratory | Formal, tested, complete |
| Flexible names (`sample.py`, `01_sample.py`) | Numbered names (`01_hello.py`) |
| Work-in-progress | Production curriculum |

### Promotion workflow (Working → Formal)

1. Identify the target `L{level}/S{session}/`.
2. Rename to `01_name.py` (next available number).
3. Add file header, clean comments, verify it runs.
4. Move to `src/L{level}/S{session}/`.
5. Reference the new file in `docs/sessions/L{level}/S{session}.md`.

### Standard file template

Modelled on the `main` / `HELP_TEXT` pattern in `src/Working/Module1/01_sample.py` and formal files such as `src/L1/S1/01_hello.py`:

```python
"""Module docstring — what this file demonstrates."""

import sys

HELP_TEXT = """script_name.py

Purpose
    One-line purpose.

Usage
    python script_name.py
"""

def main(argv: list[str]) -> int:
    if any(arg in {"-h", "--help"} for arg in argv[1:]):
        print(HELP_TEXT)
        return 0
    # implementation here
    return 0

raise SystemExit(main(sys.argv))
```

### Rules for Claude

- ✅ Apply relaxed quality expectations to `src/Working/` files
- ✅ When asked to "bucket" / promote a Working file, follow the promotion workflow
- ✅ Source-material transcripts in `source-material/` are instructor notes — use them as inspiration only; transform ideas, never copy text
- ❌ Do **not** reference `src/Working/` paths in `docs/sessions/` — only promoted `src/L{level}/S{session}/` paths belong in session docs
- ❌ Do **not** treat CI lint failures on Working files as blockers

---

## 📝 Session Documentation (`docs/sessions/`)

- Every session doc must follow the structure in `.cursor/rules/01_educational-content-rules.mdc`.
- YAML frontmatter is optional; clear headings and educational flow are mandatory.
- Practice file references point to `src/L{level}/S{session}/` only.

## 💻 Practice Code (`src/L{level}/S{session}/`)

- Files named `01_name.py`, `02_name.py`, …
- All files must run without errors.
- Include a file-header comment: `# Filename: src/L1/S2/01_variables.py`.

---

## 🔗 Related Files

- **Cursor rules:** `.cursor/rules/` — full rule set for content creation, structure, QA
- **Copilot instructions:** `.github/copilot-instructions.md`
- **Structure doc:** `docs/RepositoryStructure.md`
- **Master plan:** `docs/01_Python-Fundamentals-MasterPlan.md`
