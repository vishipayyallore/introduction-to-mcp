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
