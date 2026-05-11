# Introduction to MCP

## What is MCP?

The **Model Context Protocol (MCP)** is an open protocol that enables AI models to securely
interact with external tools, data sources, APIs, and applications through a standardized interface.

It acts as a universal integration layer between AI systems and external services, making tool
and context sharing consistent and interoperable across platforms.

## Why LLMs Need External Integration

Modern language models are powerful reasoning engines, but their knowledge is static — frozen at
training time. They cannot look up a live database, send a Slack message, or read a file that was
created today.

This creates a gap: the model can *think* about a task but cannot *act* on the real world
without extra machinery. Developers filled this gap by writing custom connectors — one for
each combination of model and external service. Every new model or service required another
connector, and none of them were reusable across projects.

## The Problem MCP Solves

Before MCP, every AI application had to build its own bespoke integrations with external systems.
Each integration was one-off, fragile, and not reusable across different AI clients or models.

Connecting an assistant to three services — a version-control system, a project tracker, and a
messaging platform — meant building three separate connectors, each wired specifically to
one model. Switch models, and you rewrote everything.

MCP replaces that with a single, shared protocol — so a tool built for one MCP-compatible host
works with any other MCP-compatible host without modification.

## Two Reasons Anthropic Built MCP

**1. Real tool-using capability**

Giving a model access to live data and actions transforms it from a static oracle into an active
participant. With MCP, the model can consult an API, trigger a workflow, or read a record that
was created seconds ago — things training data can never provide.

**2. Controlled, auditable access**

Connecting AI to live systems raises legitimate concerns about data exposure. MCP addresses this
by making access explicit: each server declares exactly what it offers, and the host decides
what the model is allowed to call. You can give a model access to your issue tracker without
also giving it access to customer records. Access boundaries are defined in code, not assumed.

## Key Properties

- **Standardized** — one protocol, many implementations
- **Secure** — explicit capability declaration; servers only expose what they choose
- **Composable** — clients can connect to multiple servers simultaneously
- **Transport-agnostic** — works over stdio, HTTP/SSE, and other transports

## MCP as a Universal Standard

The way WiFi lets every wireless device join any compatible network — regardless of manufacturer —
MCP lets any compatible AI model connect to any compatible server without custom glue code.
Implement MCP once on your service, and any model that speaks the protocol can use it.

This also scales horizontally: a single host can connect to multiple MCP servers simultaneously,
giving the model a coordinated view across systems that were previously siloed.

## Relationship to Other Standards

MCP is inspired by the Language Server Protocol (LSP), which solved a similar N×M integration
problem for editors and language tooling. MCP applies the same idea to AI and external services.

## Next

→ [MCP Architecture](../02-architecture/README.md) | ← [Setup](../00-setup/README.md)
