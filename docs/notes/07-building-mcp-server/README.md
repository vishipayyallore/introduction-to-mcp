# Building MCP Servers

## FastMCP — High-Level Abstraction

The `mcp` package ships two layers: a low-level protocol API and `FastMCP`, a high-level
decorator-based layer inspired by FastAPI. For most servers, `FastMCP` is the right starting
point — it handles capability registration, schema generation, and transport boilerplate
automatically.

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

The docstring becomes the tool description the model reads when deciding whether to call the tool.
Type annotations are converted to a JSON Schema `inputSchema` automatically.

### Resources with FastMCP

```python
@mcp.resource("data://employees/all")
def list_employees() -> list[dict]:
    """Return all employees from the database."""
    return load_employees()
```

Resources are exposed at a URI and readable by the host — useful for data that the model
should consult rather than actively compute.

---

## Project Initialization with uv

The recommended workflow for a new MCP server:

```bash
uv init my-server
cd my-server
uv add "mcp[cli]"
```

This creates a locked environment specific to the project, avoiding conflicts with other Python
projects on the same machine.

---

## Registering a Server with Claude Desktop

After writing your server, register it so Claude Desktop starts it automatically:

```bash
uv run mcp install server.py --name "My Server"
```

This writes an entry to `claude_desktop_config.json`. Restart Claude Desktop after any change
to the config file for the new server to appear.

To inspect the config manually: **Settings → Developer → Edit Config**. The entry looks like:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["run", "server.py"]
    }
  }
}
```

---

## Debugging with the MCP Log File

When a server call fails or returns unexpected results, check the Claude Desktop log file:

**Settings → Developer → Open MCP Log File**

Each log entry records the tool name, arguments, response, and any server-side errors.
This is the primary debugging surface for issues that do not reproduce in the MCP Inspector.

Common issues and fixes:

| Symptom | Likely cause | Fix |
|---|---|---|
| Server not visible in Claude Desktop | Config not saved or Claude not restarted | Restart Claude Desktop after editing config |
| Import error for `mcp` | Wrong Python interpreter selected | Choose the `.venv` entry (Ctrl+Shift+P → Select Interpreter) |
| Tool called but wrong result returned | Tool description is ambiguous | Rewrite the docstring to be more specific about when to call |
| Database errors on first call | DB not initialized before tools run | Call `init_db()` inside `if __name__ == "__main__":` before `mcp.run()` |

---

## Available SDKs

| Language | Package |
|---|---|
| Python | `mcp` (official SDK) |
| TypeScript / Node.js | `@modelcontextprotocol/sdk` |
| Others | Community SDKs (Go, Rust, Java, C#, …) |

## Minimal Python Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

app = Server("my-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="hello",
            description="Returns a greeting",
            inputSchema={"type": "object", "properties": {}, "required": []},
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "hello":
        return [types.TextContent(type="text", text="Hello from MCP!")]
    raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(stdio_server(app))
```

## Implementation Checklist

- [ ] Declare all tools with clear `name`, `description`, and `inputSchema`
- [ ] Handle unknown tool names with a clear error
- [ ] Return structured `TextContent`, `ImageContent`, or `EmbeddedResource`
- [ ] Write logs to stderr, never stdout (stdout is reserved for the protocol)
- [ ] Test with `mcp dev` or the MCP Inspector before connecting to a host

## Design Principles

- **Describe tools for the model, not for the user** — the description is what the model reads
  to decide when to call the tool; make it precise and unambiguous
- **Fail loudly** — return errors with clear messages; do not silently return empty results
- **Keep servers focused** — one server per domain (filesystem, database, API); avoid monolithic servers

## Next

→ [Real-world Use Cases](../08-real-world-use-cases/README.md)
