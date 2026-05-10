# uv commands for this repository

This project uses **[uv](https://docs.astral.sh/uv/)** for Python environments and
for running tools (including the MCP CLI) without manually activating a venv.

Install uv from the upstream docs for your OS, then use the commands below.

## `uv init`

Creates a new project layout (for example `pyproject.toml` and related defaults).
Use this when you are **starting a brand-new Python project** from an empty
directory.

**This repository already ships a `pyproject.toml`**, so you normally **do not**
run `uv init` here unless you are intentionally re-scaffolding.

New project (empty directory):

```bash
uv init
```

## `uv sync --all-groups --link-mode=copy`

Installs dependencies from the lockfile into the project environment and includes
**every optional dependency group** (for example dev or docs groups when they
exist in `pyproject.toml`).

**`--link-mode=copy`** copies files into the environment instead of hardlinking,
which avoids issues on some **Windows** and **network / shared** filesystems.

This repository (install all groups, stable linking on Windows / shared disks):

```bash
uv sync --all-groups --link-mode=copy
```

After `uv sync`, use **`uv run …`** to execute Python tools and scripts with that
environment.

## `uv run mcp`

Runs the **MCP CLI** from the installed [`mcp`](https://pypi.org/project/mcp/)
package (this project pins **`mcp[cli]`** in `pyproject.toml`). Use it for
MCP-related commands (for example inspecting help or dev tooling) without
activating the virtual environment manually:

```bash
uv run mcp --help
```

See the upstream Python SDK and CLI docs for the full command surface.

## See also

- [uv documentation](https://docs.astral.sh/uv/)
- [mcp on PyPI](https://pypi.org/project/mcp/)
