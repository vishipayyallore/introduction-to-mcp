# MCP Architecture

## Core Components

MCP defines three primary roles:

| Role | Description |
|---|---|
| **Host** | The application the user interacts with (e.g., Claude Desktop, an IDE) |
| **Client** | Lives inside the host; manages one connection to one MCP server |
| **Server** | An external process that exposes tools, resources, and prompts |

A single host can run multiple clients, each connected to a different server.

## Communication Model

```
Host
└── Client  ←──── MCP Protocol ────→  Server
└── Client  ←──── MCP Protocol ────→  Server
```

- The **host** controls what servers are connected and what permissions are granted.
- The **client** handles the protocol lifecycle with a single server.
- The **server** declares its capabilities during initialization and responds to requests.

## Capability Negotiation

On connection, client and server exchange capability declarations:

- Server announces: which tools, resources, and prompts it offers
- Client announces: which protocol features it supports (sampling, roots, etc.)

Neither side can use a capability the other hasn't declared.

## Message Types

| Type | Direction | Purpose |
|---|---|---|
| Request | Client → Server or Server → Client | Expects a response |
| Response | Reply to a request | Carries result or error |
| Notification | Either direction | One-way, no reply expected |

## Next

→ [Clients and Servers](../03-clients-and-servers/README.md)
