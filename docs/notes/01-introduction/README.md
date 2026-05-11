# Introduction to MCP

## What is MCP?

The **Model Context Protocol (MCP)** is an open protocol that enables AI models to securely
interact with external tools, data sources, APIs, and applications through a standardized interface.

It acts as a universal integration layer between AI systems and external services, making tool
and context sharing consistent and interoperable across platforms.

## The Problem MCP Solves

Before MCP, every AI application had to build its own bespoke integrations with external systems.
Each integration was one-off, fragile, and not reusable across different AI clients or models.

MCP replaces that with a single, shared protocol — so a tool built for one MCP-compatible host
works with any other MCP-compatible host without modification.

## Key Properties

- **Standardized** — one protocol, many implementations
- **Secure** — explicit capability declaration; servers only expose what they choose
- **Composable** — clients can connect to multiple servers simultaneously
- **Transport-agnostic** — works over stdio, HTTP/SSE, and other transports

## Relationship to Other Standards

MCP is inspired by the Language Server Protocol (LSP), which solved a similar N×M integration
problem for editors and language tooling. MCP applies the same idea to AI and external services.

## Next

→ [MCP Architecture](../02-architecture/README.md)
