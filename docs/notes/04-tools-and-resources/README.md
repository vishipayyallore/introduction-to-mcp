# Tools and Resources

MCP servers expose three primitives to clients: **tools**, **resources**, and **prompts**.

## Tools

Tools are callable functions the AI model can invoke to take actions or retrieve computed data.

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": { "type": "string" }
    },
    "required": ["location"]
  }
}
```

- The model decides *when* to call a tool based on its description
- The host may require user approval before execution
- Tools return structured content (text, images, embedded resources)

## Resources

Resources expose data that can be read by the client — files, database records, live system state.

- Identified by a URI (e.g., `file:///path/to/doc`, `db://table/row`)
- Can be static (read once) or dynamic (change over time)
- Clients can subscribe to resource updates when the server supports it

Resources are distinct from tools: reading a resource is a *data access*, not an *action*.

## Prompts

Prompts are pre-built message templates or workflows that servers can offer to clients.

- Help users invoke complex multi-step interactions with a single command
- Can accept arguments that get interpolated into the template
- Listed and selected by the host/user, then expanded into conversation messages

## Comparison

| Primitive | Initiated by | Purpose |
|---|---|---|
| Tool | Model | Take an action or compute a result |
| Resource | Client/Host | Read data from the server's domain |
| Prompt | User/Host | Load a pre-built interaction template |

## Next

→ [Transport Layers](../05-transports/README.md)
