# Project Tracker Demo (04)

SQLite-backed **projects** and **tickets** with many **URI templates** so clients fetch
**stable paths over evolving state** - the Demo **04** theme: **stateful, templated MCP resources**.

Tools mutate the database; **resources** are cheap read views that always reflect the latest rows.

<!-- markdownlint-disable MD013 -->

## What this teaches

| Concept | Where |
| --- | --- |
| Dynamic resource URIs (`ticket://{ticket_id}`, etc.) | `server.py` `@mcp.resource` handlers |
| URI templates listed separately from static resources | MCP Inspector + `list_resource_templates` in `client.py` |
| Stateful persistence (SQLite file next to code) | `project_tracker.db` (gitignored) |
| Tools that change data vs resources that snapshot it | `create_ticket`, `update_ticket_status` vs `tickets://…` |

## Structure

```text
04-project-tracker/
├── server.py       # FastMCP: resources + tools
├── tracker_db.py   # Schema, seed data, formatting helpers
├── client.py       # Lists templates, read_resource samples, tool demos
├── settings.py
└── config/settings.json   # port 8003
```

## Setup

```bash
uv sync
```

Uses the **repo root** `pyproject.toml` (MCP SDK). Standard library **sqlite3** only.

## Run

HTTP base URL: **`http://127.0.0.1:8003/mcp`**.

### Mode 1 - stdio, one terminal

```bash
uv run python src/demos/04-project-tracker/client.py --stdio
```

### Mode 2 - HTTP, two terminals

**Terminal 1:**

```bash
uv run python src/demos/04-project-tracker/server.py
```

**Terminal 2:**

```bash
uv run python src/demos/04-project-tracker/client.py
```

### Inspector

Same patterns as [01-calculator](../01-calculator/README.md): stdio dev server, or HTTP with **Proxy**
to `http://127.0.0.1:8003/mcp`.

## Resource URIs (cheat sheet)

| URI pattern | Purpose |
| --- | --- |
| `tickets://all` | All tickets (static listing resource) |
| `ticket://{ticket_id}` | One ticket (template) |
| `tickets://for-project/{project_id}` | Tickets for project id `PROJ001`, … |
| `tickets://status/{status}` | `pending`, `in_progress`, … |
| `tickets://assignee/{assignee}` | By assignee name |
| `projects://all` | All projects + ticket counts |
| `project://{project_id}` | Project detail + status breakdown |

Project-scoped tickets use **`project_id`** in the path so URIs stay simple (no spaces), while the
`project` column on tickets remains the human-readable project **name**.

## Tools

| Tool | Role |
| --- | --- |
| `create_ticket` | Insert a new pending ticket |
| `update_ticket_status` | Move along workflow (`pending` / `in_progress` / `completed` / `closed`) |

## Relationship to other demos

- **03** emphasized **async** tools; this demo uses **sync** tools so the lesson stays on
  **resources + templates + DB state**.
- **05** can build multi-step workflows that chain these tools.

<!-- markdownlint-enable MD013 -->
