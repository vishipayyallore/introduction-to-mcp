# Real-world Use Cases

## Categories of MCP Servers

### Data Access

| Use case | What the server exposes |
|---|---|
| File system | Read/write local files and directories |
| Database | Query tables, run SQL, read schemas |
| Knowledge base | Search documents, retrieve embeddings |

### External Services

| Use case | What the server exposes |
|---|---|
| Web search | Search queries, page fetch |
| Calendar / email | Read events, draft messages |
| Version control | Read diffs, list PRs, create issues |

### Developer Tools

| Use case | What the server exposes |
|---|---|
| Code execution | Run scripts, return stdout/stderr |
| Test runner | Execute tests, report results |
| Build system | Trigger builds, read logs |

## Patterns

### Wrapping an Existing API

The most common pattern: take a REST API and expose its endpoints as MCP tools.
Each endpoint becomes a tool with a schema derived from the API's request body.

### Stateful Context Servers

Servers that maintain state across calls — for example, a server that tracks a shopping cart
or holds a database cursor open across multiple queries.

### Chained Servers

Hosts can connect to multiple servers simultaneously. The model can call tools across servers
in a single conversation — for example, reading from a database server and then writing to
a file system server in one workflow.

## Reference Projects

The following two projects illustrate how the patterns above translate into working servers.
Both use SQLite for local storage and Claude Desktop as the client.

---

### Leave Manager Server

**Goal:** Let an AI assistant handle leave requests on behalf of a team — submitting, approving,
denying, and checking balances — through natural-language conversation.

**Architecture:**

```
Claude Desktop (client)
       │  natural-language request
       ▼
MCP Protocol
       │  resolves to a tool or resource
       ▼
Leave Manager Server
       │  SQL query
       ▼
SQLite DB (employees + leave_requests tables)
```

**Data model:**
- `employees` — id, name, department, manager, sick_leave_balance, general_leave_balance
- `leave_requests` — request_id, employee_id, start_date, end_date, type, status

**Tools (write operations):**

| Tool | What it does |
|---|---|
| `submit_leave_request` | Validates leave balance and inserts a new request |
| `approve_leave_request` | Sets status to approved for a given request ID |
| `deny_leave_request` | Sets status to denied with an optional reason |
| `add_employee` | Inserts a new employee record |

**Resources (read operations):**

| Resource URI | What it returns |
|---|---|
| `employees://all` | All employees |
| `employees://{id}` | One employee by ID |
| `leaves://all` | All leave requests |
| `leaves://employee/{id}` | Leaves for one employee |
| `leaves://pending` | Requests awaiting approval |

**Key design decisions:**
- Resources for reads, tools for writes — this keeps read-only queries cheaper
  (no tool-call cost) and separates query intent from mutation intent.
- Leave balance check happens inside `submit_leave_request` before insert — the server
  enforces the rule, not the model.
- The DB is created with sample data on first run if it does not already exist.

---

### Project Management Server

**Goal:** Give an AI assistant full visibility into a project tracker — creating tickets, updating
status, assigning work, and querying overdue items through conversation.

**Architecture:** Identical to the leave manager — Claude Desktop → MCP → server → SQLite.

**Data model:**
- `projects` — id, name, description, owner, created_at
- `tickets` — id, project_id, title, description, status, priority, assignee, due_date, tags

**Tools:**

| Tool | What it does |
|---|---|
| `create_ticket` | Adds a ticket to a project |
| `update_ticket_status` | Changes a ticket's status |
| `assign_ticket` | Sets the assignee |
| `create_project` | Adds a project |
| `search_tickets` | Full-text search across title and description |
| `get_overdue_tickets` | Returns tickets past their due date |
| `update_ticket_priority` | Changes priority level |
| `add_ticket_tags` | Appends tags to an existing ticket |

**Resources:**

| Resource URI | What it returns |
|---|---|
| `tickets://all` | All tickets |
| `tickets://{id}` | One ticket by ID |
| `projects://all` | All projects |
| `projects://{name}` | One project by name |
| `tickets://status/{status}` | Tickets filtered by status |
| `tickets://assignee/{name}` | Tickets for a specific person |

**Lessons from building this server:**
- Initialize the database *before* registering tools. If `init_db()` is called after
  `mcp.run()`, tools may fire before the schema exists.
- When the model uses the wrong tool for a query, the tool description is usually the cause —
  not the model. Make descriptions unambiguous about input format and expected output.
- Use the MCP log file (Claude Desktop → Developer → Open MCP Log File) to confirm which
  tool was called and what arguments were passed.

---

## Evaluating Whether to Build an MCP Server

Build one when:
- The capability is reusable across multiple AI workflows
- The data source or API is not already natively accessible to the host
- The integration requires stateful context or streaming data

Use a simpler tool-call integration when:
- The integration is one-off and host-specific
- The capability is already provided by the host natively

## Back to Start

→ [Introduction](../01-introduction/README.md) | [Index](../README.md)
