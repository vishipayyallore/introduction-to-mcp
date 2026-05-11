# Leave Manager Demo (03)

SQLite-backed **leave requests** and **employee directory** with **async MCP tools**.

This folder builds on [01-calculator](../01-calculator/README.md) (transports, Inspector) and
[02-typed-calculator](../02-typed-calculator/README.md) (structured contracts), and focuses
Demo **03** on **`async def` tools**, simulated latency, and **`asyncio.to_thread`** for
blocking SQLite — so the asyncio event loop stays usable while work hits the database.

<!-- markdownlint-disable MD013 -->

## What this teaches

| Concept | Where |
| --- | --- |
| Async tools (`async def` + `await`) | `server.py` |
| Simulated HR / API latency (`asyncio.sleep`) | `_SIM_*` constants in `server.py` |
| Blocking I/O off the event loop (`asyncio.to_thread`) | Tool implementations calling `leave_db.py` |
| Dynamic resources with URI parameters | `employee://{id}`, `leave-requests://…` |
| Stateful persistence | `leave_manager.db` (SQLite, gitignored) |

## Structure

```text
03-leave-manager/
├── server.py       # FastMCP app: async tools + sync resources
├── leave_db.py     # Dataclasses, schema init, seed data, sync DB helpers
├── client.py       # Sample session over HTTP or stdio
├── settings.py     # Shared JSON config loader
└── config/
    └── settings.json   # port 8002 by default
```

The database file **`leave_manager.db`** is created next to these modules on first run (see
`.gitignore`).

## Setup

From the repo root:

```bash
uv sync
```

Uses the repo `pyproject.toml` (MCP SDK + Pydantic). **SQLite**, **difflib**, and **asyncio**
are in the standard library.

## Run

Default HTTP URL: **`http://127.0.0.1:8002/mcp`** (won’t collide with demos **01** / **02**).

### Mode 1 — stdio, one terminal

```bash
uv run python src/demos/03-leave-manager/client.py --stdio
```

### Mode 2 — HTTP, two terminals

**Terminal 1:**

```bash
uv run python src/demos/03-leave-manager/server.py
```

**Terminal 2:**

```bash
uv run python src/demos/03-leave-manager/client.py
```

### Inspector — stdio

```bash
uv run mcp dev src/demos/03-leave-manager/server.py
```

Use **Transport Type: STDIO**. Tools registered as `async` appear like any other tool; try
calling **`submit_leave_request`** and **`approve_leave_request`** while watching timing.

### Inspector — Streamable HTTP

Start the HTTP server first, then `mcp dev` with **URL** `http://127.0.0.1:8002/mcp` and
**Proxy** — same pattern as [01-calculator](../01-calculator/README.md).

## Tools (all async in this demo)

| Tool | Role |
| --- | --- |
| `submit_leave_request` | Insert pending request |
| `approve_leave_request` | Approve + decrement balances for annual/sick |
| `check_leave_balance` | Read balances for one employee |
| `get_pending_approvals` | List pending rows |
| `get_database_stats` | Aggregate counts |
| `add_employee` | Add employee with fuzzy duplicate hints |

## Resources

| URI pattern | Purpose |
| --- | --- |
| `employees://all` | Full directory |
| `employee://{employee_id}` | One employee |
| `leave-requests://all` | All requests |
| `leave-requests://employee/{employee_id}` | Per employee |
| `leave-requests://status/{status}` | Filter by status |

## Relationship to other demos

- **01** — Primitive calculator; transport patterns reused here unchanged.
- **02** — Pydantic-heavy contracts; this demo keeps plain tool parameters for readability while
  teaching **async** execution.

## Roadmap

Continue with **[04-project-tracker](../04-project-tracker/README.md)** for Demo **04**
(stateful SQLite + many URI templates). **Production** SQLite usage would typically move to
connection pooling or `aiosqlite`.

<!-- markdownlint-enable MD013 -->
