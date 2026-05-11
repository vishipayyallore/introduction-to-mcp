# Clients and Servers

## The Client Role

An MCP client:

- Is created and managed by the host application
- Maintains exactly one connection to one MCP server
- Handles the protocol handshake and capability negotiation
- Routes requests from the host to the server and surfaces responses

The client is a protocol adapter — it does not contain business logic about what the tools do.

## The Server Role

An MCP server:

- Runs as a separate process (local or remote)
- Exposes a fixed set of **tools**, **resources**, and **prompts** to clients
- Declares all capabilities upfront during initialization
- Processes requests and returns structured responses

Servers are stateless with respect to conversation history — they respond to individual requests
and do not hold conversational context.

## Lifecycle

```
1. Host starts server process
2. Client sends `initialize` request
3. Server responds with its capabilities
4. Client sends `initialized` notification
5. Normal operation: requests and responses
6. Either side sends `shutdown`, then connection closes
```

## Server Boundaries

Each server is an isolated process with its own permissions and trust level. The host decides:

- Which servers to connect to
- What data to share with each server
- Whether to approve tool calls before execution

## Next

→ [Tools and Resources](../04-tools-and-resources/README.md)
