# MCP Learning Notes

A structured collection of theory and conceptual notes on the Model Context Protocol (MCP).

## Topics

- [Setup](setup/README.md) — Python, uv, Claude Desktop, and the MCP package
1. [Introduction](01-introduction/README.md) — What MCP is, why it exists, and the problem it solves
2. [MCP Architecture](02-architecture/README.md) — Core design, components, and how they interact
3. [Clients and Servers](03-clients-and-servers/README.md) — Roles, responsibilities, and lifecycle
4. [Tools and Resources](04-tools-and-resources/README.md) — Primitives exposed by MCP servers
5. [Transport Layers](05-transports/README.md) — stdio, HTTP/SSE, and how messages flow
6. [Security](06-security/README.md) — Trust boundaries, authorization, and safe practices
7. [Building MCP Servers](07-building-mcp-server/README.md) — Implementation patterns and SDKs
8. [Real-world Use Cases](08-real-world-use-cases/README.md) — Practical applications and examples

## Structure

```text
docs/
├── images/          # diagrams and screenshots
└── notes/           # theory and conceptual notes (this folder)
    ├── setup/
    ├── 01-introduction/
    ├── 02-architecture/
    ├── 03-clients-and-servers/
    ├── 04-tools-and-resources/
    ├── 05-transports/
    ├── 06-security/
    ├── 07-building-mcp-server/
    └── 08-real-world-use-cases/
```

Experiments and prototypes live in `src/`.
