# Typed Calculator Demo (02)

<!-- markdownlint-disable MD013 -->

Same calculator behavior as [01-calculator](../01-calculator/README.md), but tools use
**Pydantic** `BinaryOpRequest` / `BinaryOpResponse` models instead of bare floats.

This demo answers the review feedback that typed contracts belong in **Demo 02**, not
by refactoring Demo 01 — keeping **01** small and **02** focused on schemas.

## What this teaches

| Concept | Where |
| --- | --- |
| Structured tool input/output (JSON Schema from Pydantic) | `models.py`, `server.py` |
| Field descriptions that appear in MCP schemas | `BinaryOpRequest`, `BinaryOpResponse` |
| Single-parameter tool objects (`request: BinaryOpRequest`) | `@mcp.tool()` handlers |
| Optional tool metadata (`title`, `ToolAnnotations`) | `add` tool in `server.py` |
| Resources + prompts (same pattern as 01, new URI prefix) | `typed-calculator://help` |
| HTTP + stdio transports | `config/settings.json` (port **8001**) |

## Why typed models

- Clients and agents see **explicit JSON Schemas** in the MCP Inspector.
- **Validation** runs before your Python code (invalid inputs fail fast).
- Matches how **production MCP servers** expose structured contracts.

## Structure

```text
02-typed-calculator/
├── models.py          # BinaryOpRequest, BinaryOpResponse
├── server.py          # Tools return BinaryOpResponse; add() shows metadata
├── client.py          # Calls tools with {"request": {"a": ..., "b": ...}}
├── settings.py        # Shared JSON config loader (same pattern as 01)
└── config/
    └── settings.json  # host 127.0.0.1, port 8001 — avoids clashing with Demo 01
```

## Setup

From the repo root:

```bash
uv sync
```

Dependencies include the MCP SDK (which brings **Pydantic**). No extra install step.

## Run

Default transport is **streamable-http** from `config/settings.json`. This server listens on
**port 8001** so you can run **01** and **02** HTTP servers at the same time.

### Mode 1 — stdio, one terminal

```bash
uv run python src/demos/02-typed-calculator/client.py --stdio
```

### Mode 2 — HTTP, two terminals

**Terminal 1:**

```bash
uv run python src/demos/02-typed-calculator/server.py
```

**Terminal 2:**

```bash
uv run python src/demos/02-typed-calculator/client.py
```

HTTP endpoint: `http://127.0.0.1:8001/mcp`.

### Mode 3 — MCP Inspector (stdio)

```bash
uv run mcp dev src/demos/02-typed-calculator/server.py
```

Use **Transport Type: STDIO**. Inspect the **Tools** tab to see schemas derived from the
Pydantic models.

### Mode 4 — MCP Inspector (Streamable HTTP)

Start the HTTP server (Terminal 1), then:

```bash
uv run mcp dev src/demos/02-typed-calculator/server.py
```

Set transport to **Streamable HTTP**, URL **`http://127.0.0.1:8001/mcp`**, **Connection Type:
Proxy** — same rationale as Demo 01 (see [01-calculator README](../01-calculator/README.md)).

## Client argument shape

Tools are declared as `def add(request: BinaryOpRequest) -> BinaryOpResponse`. The MCP layer
expects arguments keyed by the parameter name:

```json
{
  "request": { "a": 10, "b": 3 }
}
```

The sample client in `client.py` uses that shape for every operation.

## Validation try-it-yourself

In the Inspector, call `add` with invalid input (for example omit `b` or use a non-number).
Compare the validation error to Demo 01’s float-only parameters.

## Tools exposed

| Tool | Arguments | Returns |
| --- | --- | --- |
| `add` | `request` (`a`, `b` floats) | `{ "result": float }` |
| `subtract` | same | same |
| `multiply` | same | same |
| `divide` | same | error if `b == 0` |

## Roadmap (later demos)

As suggested in curriculum review — **not** part of this folder:

| Topic | Planned demo |
| --- | --- |
| Logging / tracing middleware | Later (e.g. production-focused demo) |
| `async` tools + delays | [Demo 03 — Leave Manager](../03-leave-manager/README.md) |
| Stateful / templated resources | Demo 04 |
| Shared config package beyond JSON loader | Optional refactor when multiple demos need it |

## Relationship to Demo 01

**01** stays intentionally minimal (primitive types, maximum readability).

**02** adds **one** major idea: **structured contracts**. Transport choice and client/server
layout stay the same.

<!-- markdownlint-enable MD013 -->
