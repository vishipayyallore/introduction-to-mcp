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
├── requirements.txt   # Python dependencies
└── config/
    └── settings.json  # Server metadata (name, version, transport)
```

## Setup

```bash
cd src/demos/01-calculator
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

**Terminal 1 — start the server (serves on http://localhost:8000/mcp):**

```bash
python server.py
```

**Terminal 2 — run the client:**

```bash
python client.py
```

**Or inspect interactively with the MCP CLI:**

```bash
mcp dev server.py
```

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
