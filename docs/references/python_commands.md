# Python commands for this repository

This project requires **Python 3.11+** and uses `uv run python` to target the
project virtual environment without manually activating it.

---

## Version check

Confirm the active interpreter meets the minimum requirement:

```bash
python --version
```

Via `uv` (uses the project environment):

```bash
uv run python --version
```

---

## `python -m compileall`

Byte-compiles all `.py` files in a directory tree. Use this to surface syntax
errors across the entire source tree before running anything.

Compile everything under `src/` (quiet — errors only):

```bash
uv run python -m compileall -q src/
```

Compile a single demo:

```bash
uv run python -m compileall -q src/demos/01-calculator/
```

A clean run produces no output. Any `SyntaxError` is reported with the file
path and line number.

---

## Running demo servers

Each demo ships its own `server.py`. Start a server with:

```bash
uv run python src/demos/01-calculator/server.py
uv run python src/demos/02-typed-calculator/server.py
uv run python src/demos/03-leave-manager/server.py
```

Override transport at runtime:

```bash
uv run python src/demos/01-calculator/server.py --transport stdio
```

---

## Running demo clients

HTTP client (server must already be running):

```bash
uv run python src/demos/01-calculator/client.py
uv run python src/demos/02-typed-calculator/client.py
uv run python src/demos/03-leave-manager/client.py
```

Stdio client (starts the server as a subprocess automatically):

```bash
uv run python src/demos/01-calculator/client.py --stdio
uv run python src/demos/02-typed-calculator/client.py --stdio
uv run python src/demos/03-leave-manager/client.py --stdio
```

---

## `python -m ruff` (via uv run)

`ruff` is not installed globally; run it through `uv`:

```bash
uv run ruff check src/
```

Fix auto-fixable issues in place:

```bash
uv run ruff check --fix src/
```

---

## See also

- [`uv-commands.md`](uv-commands.md) — environment management and MCP CLI
- [Python docs: compileall](https://docs.python.org/3/library/compileall.html)
- [Ruff documentation](https://docs.astral.sh/ruff/)
