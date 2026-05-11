# MCP Demos

Hands-on demos for learning Model Context Protocol (MCP) patterns with FastMCP and
related tooling. Each demo is self-contained; later demos build on the foundation
laid by the previous one by adding exactly one new concept.

## Core idea

> **Transport is orthogonal to tool logic.**

The same tool definition runs identically over `stdio` or `streamable-http`.
Every demo reinforces this mental model.

## Learning progression

| Demo | Folder | Topic | Key concepts |
| --- | --- | --- | --- |
| 01 | [01-calculator](01-calculator/) | Basic FastMCP calculator | Tools, resources, prompts, HTTP + stdio transports, client sessions, MCP Inspector |
| 02 | — | Typed contracts + validation | Pydantic models, schema generation, structured request/response |
| 03 | — | Async tools | Async tool functions, concurrency, long-running operations |
| 04 | — | Stateful resources | Dynamic resource URIs, URI templating, session state |
| 05 | — | Multi-tool orchestration | Tool composition, sequencing, agent-driven chaining |
| 06 | — | External API integration | HTTP clients, retries, error propagation |
| 07 | — | Authentication | API keys, bearer tokens, secure credential handling |
| 08 | — | Streaming responses | Incremental tool output, streaming MCP responses |
| 09 | — | Agentic workflows | Multi-step reasoning, tool chaining, state management |
| 10 | — | Production deployment | Logging, observability, configuration, deployment patterns |
