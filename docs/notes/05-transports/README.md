# Transport Layers

MCP is transport-agnostic. The protocol defines message format and semantics; the transport
defines how those messages travel between client and server.

## stdio (Standard I/O)

The most common transport for local servers.

- Server runs as a child process of the host
- Client writes JSON-RPC messages to the server's stdin
- Server writes responses to stdout
- stderr is reserved for server logs (not protocol messages)

**Use when:** the server runs locally on the same machine as the host.

## HTTP with SSE (Server-Sent Events)

Used for remote servers accessible over a network.

- Client sends requests via HTTP POST to the server's endpoint
- Server streams responses and notifications back via SSE
- Enables servers hosted as web services

**Use when:** the server is remote, shared across clients, or deployed as a cloud service.

## Message Format

All transports carry **JSON-RPC 2.0** messages:

```json
// Request
{ "jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": { ... } }

// Response
{ "jsonrpc": "2.0", "id": 1, "result": { ... } }

// Notification (no id, no reply expected)
{ "jsonrpc": "2.0", "method": "notifications/tools/list_changed" }
```

## Choosing a Transport

| Scenario | Transport |
|---|---|
| Local CLI tool or file system access | stdio |
| Shared service, remote API, cloud deployment | HTTP + SSE |
| Testing / in-process (same language, same process) | In-memory (SDK-specific) |

## Next

→ [Security](../06-security/README.md)
