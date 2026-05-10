# Security

## Trust Boundaries

MCP defines clear trust levels across its three roles:

| Role | Trust level |
|---|---|
| Host | Fully trusted — controls all connections and permissions |
| Client | Trusted within the host's sandbox |
| Server | **Untrusted by default** — treated as a third-party process |

The host is the security boundary. It decides what servers to connect, what data to share,
and whether to approve tool calls before they execute.

## Principle of Least Privilege

Servers should only request the capabilities they need. Clients should:

- Grant servers access only to the resources they explicitly require
- Never expose raw API keys or credentials directly to server processes
- Scope permissions per-server, not globally

## Tool Call Approval

Hosts should surface tool calls to the user before execution when the action is:

- Irreversible (deleting files, sending messages, modifying data)
- Affects systems outside the user's local environment
- Initiated without clear user intent in the current context

## Prompt Injection Risks

Because MCP servers can return arbitrary text (including tool results), malicious content in
external data could attempt to hijack model behavior. Mitigations:

- Treat all server-returned content as untrusted user data, not instructions
- Hosts should not blindly execute tool calls suggested by tool *results*
- Validate that tool calls match the declared schema

## Server Identity

When connecting to remote servers, verify:

- The server's origin matches the expected host/domain
- TLS is used for HTTP transport
- Authentication tokens are scoped and rotatable

## Next

→ [Building MCP Servers](../07-building-mcp-server/README.md)
