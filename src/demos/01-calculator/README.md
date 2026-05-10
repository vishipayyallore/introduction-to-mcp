# Calculator Demo

A minimal MCP server and client demonstrating core protocol concepts using a four-function calculator.

## What this teaches

- MCP server lifecycle (init → capability negotiation → tool calls → shutdown)
- Tool registration with typed input schemas
- Request / response handling
- Client-server interaction over stdio transport
- Structured tool schemas and error handling

## Structure

```text
01-calculator/
├── server.py          # MCP server exposing add, subtract, multiply, divide
├── client.py          # MCP client that calls the server tools
├── requirements.txt   # Python dependencies
└── config/
    └── settings.json  # Server name, version, transport config
```

## Setup

```bash
cd src/demos/01-calculator
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

Start the server and client together (client launches server as a subprocess):

```bash
python client.py
```

Or inspect the server interactively with the MCP CLI:

```bash
mcp dev server.py
```

## Tools exposed

| Tool | Inputs | Description |
|---|---|---|
| `add` | `a`, `b` (number) | Returns a + b |
| `subtract` | `a`, `b` (number) | Returns a − b |
| `multiply` | `a`, `b` (number) | Returns a × b |
| `divide` | `a`, `b` (number) | Returns a ÷ b; errors on b = 0 |
