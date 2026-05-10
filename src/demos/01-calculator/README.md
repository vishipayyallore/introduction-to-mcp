# Calculator Demo

A minimal MCP server and client using **FastMCP** — the high-level Python API for building
MCP servers with decorators.

## What this teaches

| Concept | Where |
|---|---|
| Server lifecycle (init → negotiate → serve) | `server.py` startup |
| Tool registration with type inference | `@mcp.tool()` decorators |
| Resource exposure | `@mcp.resource()` decorator |
| Prompt templates | `@mcp.prompt()` decorator |
| Streamable-HTTP transport | `mcp.run(transport="streamable-http")` |
| Client connection and tool calls | `client.py` |

## Structure

```text
01-calculator/
├── server.py          # FastMCP server: 4 tools, 1 resource, 1 prompt
├── client.py          # HTTP client: lists capabilities, calls all tools
└── config/
    └── settings.json  # host, port, transport, server name
```

## Setup

Dependencies are managed at the repo root via `pyproject.toml` (`mcp[cli]==1.27.1`).
No separate install step is needed — `uv` resolves everything automatically.

```bash
# From the repo root — install dependencies if not already done:
uv sync
```

## Run

**Terminal 1 — start the server (serves on http://127.0.0.1:8000/mcp):**

```bash
uv run python src/demos/01-calculator/server.py
```

**Terminal 2 — run the client:**

```bash
uv run python src/demos/01-calculator/client.py
```

**Or inspect interactively with the MCP CLI:**

```bash
uv run mcp dev src/demos/01-calculator/server.py
```

Host, port, and transport are read from `config/settings.json`.

## FastMCP vs low-level Server API

| | FastMCP | `mcp.server.Server` |
|---|---|---|
| Tool definition | `@mcp.tool()` — type hints inferred as schema | Manual JSON Schema |
| Resource definition | `@mcp.resource("uri://pattern")` | Manual handler registration |
| Prompt definition | `@mcp.prompt()` | Manual handler registration |
| Transport | `mcp.run(transport=...)` | `stdio_server(app)` / custom |
| Best for | Learning, rapid prototyping | Fine-grained control |

## Tools exposed

| Tool | Inputs | Description |
|---|---|---|
| `add` | `a`, `b` (float) | Returns a + b |
| `subtract` | `a`, `b` (float) | Returns a − b |
| `multiply` | `a`, `b` (float) | Returns a × b |
| `divide` | `a`, `b` (float) | Returns a ÷ b; errors if b = 0 |

## Resource and Prompt

- **`calculation://help`** — plain-text reference guide for the tools
- **`evaluate(expression)`** — generates a prompt asking the model to solve an expression
  using only the calculator tools
