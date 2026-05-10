"""MCP calculator server — exposes add, subtract, multiply, divide as tools."""

import asyncio
import json
import logging
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# Load config from sibling config/settings.json
_config_path = Path(__file__).parent / "config" / "settings.json"
_config = json.loads(_config_path.read_text())

logging.basicConfig(level=_config["log_level"], stream=sys.stderr)
log = logging.getLogger(__name__)

app = Server(_config["server"]["name"])


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="add",
            description="Add two numbers and return the result.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First operand"},
                    "b": {"type": "number", "description": "Second operand"},
                },
                "required": ["a", "b"],
            },
        ),
        types.Tool(
            name="subtract",
            description="Subtract b from a and return the result.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Minuend"},
                    "b": {"type": "number", "description": "Subtrahend"},
                },
                "required": ["a", "b"],
            },
        ),
        types.Tool(
            name="multiply",
            description="Multiply two numbers and return the result.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First factor"},
                    "b": {"type": "number", "description": "Second factor"},
                },
                "required": ["a", "b"],
            },
        ),
        types.Tool(
            name="divide",
            description="Divide a by b and return the result. Errors if b is zero.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Dividend"},
                    "b": {"type": "number", "description": "Divisor (must not be zero)"},
                },
                "required": ["a", "b"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    a = arguments["a"]
    b = arguments["b"]

    if name == "add":
        result = a + b
    elif name == "subtract":
        result = a - b
    elif name == "multiply":
        result = a * b
    elif name == "divide":
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        result = a / b
    else:
        raise ValueError(f"Unknown tool: {name!r}")

    log.info("%s(%s, %s) = %s", name, a, b, result)
    return [types.TextContent(type="text", text=str(result))]


if __name__ == "__main__":
    asyncio.run(stdio_server(app))
