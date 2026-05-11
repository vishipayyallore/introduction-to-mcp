# MCP demos

Hands-on demos for learning Model Context Protocol (MCP) patterns using
FastMCP, MCP Inspector, Streamable HTTP, stdio transport, and production-style
server design.

The repository progresses from foundational MCP concepts to advanced
agent-oriented and production deployment patterns.

---

## Learning goals

These demos are designed to teach:

- MCP server lifecycle
- Tool registration and schema generation
- Resources and prompt templates
- stdio vs Streamable HTTP transports
- Client/server communication patterns
- Structured contracts and validation
- Async and streaming workflows
- Stateful MCP architectures
- Multi-tool orchestration
- Agentic execution patterns
- Production deployment considerations

---

## Demo progression

<!-- markdownlint-disable MD013 -->

| Demo | Topic | What you learn |
| --- | --- | --- |
| 01 | [Basic FastMCP calculator](01-calculator/) | Build a minimal FastMCP server with tools, resources, prompts, and dual transport support (stdio + Streamable HTTP). Learn MCP fundamentals and Inspector workflows. |
| 02 | [Typed contracts + validation](02-typed-calculator/) | Use Pydantic request/response models for structured tool contracts, schema generation, validation, and typed MCP interactions. |
| 03 | Async tools | Implement async MCP tools with `async/await`, background operations, concurrency, cancellation handling, and latency-aware workflows. |
| 04 | Stateful resources | Build dynamic resources with URI parameters, session-aware state, calculation history, and contextual resource retrieval. |
| 05 | Multi-tool orchestration | Coordinate multiple MCP tools in a single workflow, compose tool pipelines, and manage intermediate execution state. |
| 06 | External API integration | Connect MCP tools to REST APIs, databases, and third-party services with retries, timeouts, serialization, and error handling. |
| 07 | Authentication | Add API keys, bearer tokens, environment-based secrets, authorization middleware, and secure transport practices. |
| 08 | Streaming responses | Stream incremental outputs, partial tool responses, progress updates, and long-running operation results over MCP transports. |
| 09 | Agentic workflows | Build agent-style systems that plan, select tools, maintain memory, and execute multi-step reasoning workflows through MCP. |
| 10 | Production deployment | Prepare MCP servers for production with structured logging, observability, Docker deployment, reverse proxies, scaling, monitoring, and operational hardening. |

<!-- markdownlint-enable MD013 -->

---

## Repository philosophy

The demos intentionally progress from:

```text
Minimal → Structured → Stateful → Distributed → Production-ready
```

Each demo introduces one major architectural concept at a time while keeping
the implementation focused and approachable.

---

## Recommended learning order

If you are new to MCP, follow the demos sequentially:

```text
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10
```

The later demos assume familiarity with concepts introduced earlier.

---

## Core technologies

This repository uses:

- FastMCP
- MCP Inspector
- Python 3.12+
- uv
- Streamable HTTP transport
- stdio transport
- Pydantic
- asyncio

---

## Running demos

Most demos support one or both of the following transports:

### stdio transport

Best for:

- Local development
- MCP Inspector
- Subprocess clients
- Learning/debugging

### Streamable HTTP transport

Best for:

- Remote clients
- Browser tooling
- Service-oriented architectures
- Production deployment

---

## Intended audience

This repository is designed for:

- AI engineers
- Platform engineers
- Agent framework developers
- Tooling architects
- Backend engineers learning MCP
- Developers building LLM-integrated systems

---

## Goal of the repository

The objective is not just to demonstrate MCP syntax, but to teach the
architectural patterns required to design robust, observable, and scalable
Model Context Protocol systems.
