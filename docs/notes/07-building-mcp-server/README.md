# Building MCP Servers

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
