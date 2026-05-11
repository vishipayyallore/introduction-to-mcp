# Setting Up Your MCP Development Environment

Before building or running MCP servers, you need four core tools and one optional package.

---

## 1. Python

MCP server logic is written in Python. Install the latest stable release from
[python.org/downloads](https://www.python.org/downloads/).

**Windows:** During installation, enable the **"Add Python to PATH"** checkbox.
This allows `python` and `pip` to run from any terminal.

Verify after install:

```bash
python --version
```

---

## 2. Code Editor

Any editor works. VS Code and Cursor are common choices because they provide
Python IntelliSense, terminal integration, and MCP server debugging support.

No special editor configuration is required to get started.

---

## 3. uv — Package and Project Manager

`uv` is a fast Python package manager that handles virtual environments and
dependency resolution. It replaces the need to manually create venvs and run
`pip install` for each project.

Install on **macOS / Linux**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install on **Windows**:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```bash
uv --version
```

See [`docs/references/uv-commands.md`](../../references/uv-commands.md) for a full command reference.

---

## 4. Claude Desktop

Claude Desktop acts as the **MCP client** for local testing. It connects to your
server process and makes its tools available in the chat interface.

Download from [claude.ai](https://claude.ai/download). After installing:

1. Open Claude Desktop settings.
2. Enable **Developer Mode** (Settings → Developer).
3. Use **Edit Config** to open `claude_desktop_config.json` — this file
   declares which MCP servers Claude should start automatically.

---

## 5. MCP Python Package (optional global install)

The `mcp` package is installed per project by `uv add mcp[cli]` (shown in the
next section). If you want the CLI available globally for quick inspection:

```bash
pip install "mcp[cli]"
```

Claude Desktop resolves MCP servers using your system Python by default, so a
global install ensures `mcp` is always reachable.

---

## Creating a New MCP Project

The standard initialization workflow using `uv`:

```bash
# 1. Create a new project folder and enter it
uv init my-mcp-server
cd my-mcp-server

# 2. Add the MCP CLI dependency
uv add "mcp[cli]"

# 3. Verify the CLI installed correctly
uv run mcp version

# 4. Create your server entry point
touch server.py
```

This creates a `pyproject.toml`, a `.venv/` virtual environment, and all the
scaffolding your server needs.

---

## Development vs Production Workflow

| Task | Command |
|---|---|
| Run server in MCP Inspector | `uv run mcp dev server.py` |
| Register server with Claude Desktop | `uv run mcp install server.py --name "My Server"` |
| Run server directly | `uv run server.py` |

`mcp dev server.py` starts an interactive inspector session at `localhost:6274`
where you can call tools and inspect request/response pairs without a full
Claude Desktop session. Use this during development before registering with
Claude Desktop.

---

## Virtual Environment Tips

`uv` manages the `.venv` automatically. If your editor or Claude Desktop reports
import errors for `mcp`:

- In VS Code / Cursor: open the command palette and run **Select Interpreter**,
  then choose the `.venv` entry that matches your project folder.
- Verify the environment is active in your terminal: the prompt should show
  `(.venv)` at the start.

---

## Next

→ [Introduction to MCP](../01-introduction/README.md)
