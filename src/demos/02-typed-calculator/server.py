"""Typed calculator MCP server — Pydantic request/response models + FastMCP.

HTTP mode (default — http://127.0.0.1:8001/mcp):
    uv run python src/demos/02-typed-calculator/server.py

Stdio mode:
    uv run python src/demos/02-typed-calculator/server.py --transport stdio
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from models import BinaryOpRequest, BinaryOpResponse
from settings import load_config

_CONFIG = load_config()

mcp = FastMCP(
    _CONFIG["server"]["name"],
    host=_CONFIG["host"],
    port=_CONFIG["port"],
    log_level=_CONFIG["log_level"],
    json_response=True,
)


# --- Tools -------------------------------------------------------------------


@mcp.tool(
    title="Add two numbers",
    description="Returns a + b using a structured request and response model.",
    annotations=ToolAnnotations(
        title="Addition", readOnlyHint=True, idempotentHint=True
    ),
)
def add(request: BinaryOpRequest) -> BinaryOpResponse:
    """Add two numbers and return the result."""
    return BinaryOpResponse(result=request.a + request.b)


@mcp.tool()
def subtract(request: BinaryOpRequest) -> BinaryOpResponse:
    """Subtract b from a and return the result."""
    return BinaryOpResponse(result=request.a - request.b)


@mcp.tool()
def multiply(request: BinaryOpRequest) -> BinaryOpResponse:
    """Multiply two numbers and return the result."""
    return BinaryOpResponse(result=request.a * request.b)


@mcp.tool()
def divide(request: BinaryOpRequest) -> BinaryOpResponse:
    """Divide a by b. Raises an error if b is zero."""
    if request.b == 0:
        raise ValueError("Division by zero is not allowed.")
    return BinaryOpResponse(result=request.a / request.b)


# --- Resources ---------------------------------------------------------------


@mcp.resource("typed-calculator://help")
def calculation_help() -> str:
    """Reference guide for the typed calculator tools."""
    return (
        "Tools accept a single argument object `request` "
        "with fields `a` and `b` (floats).\n"
        "Each tool returns a structured object with `result` (float).\n"
        "divide raises an error when b is 0.\n"
        "Open the MCP Inspector to inspect generated JSON Schemas."
    )


# --- Prompts -----------------------------------------------------------------


@mcp.prompt()
def evaluate(expression: str) -> str:
    """Prompt the model to evaluate an expression using the calculator tools."""
    return (
        f"Evaluate the following expression using only the available calculator tools "
        f"(add, subtract, multiply, divide). "
        f"Each tool takes request {{a, b}}: {expression}"
    )


# --- Entry point -------------------------------------------------------------


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Typed calculator MCP server (FastMCP)."
    )
    parser.add_argument(
        "--transport",
        default=None,
        metavar="NAME",
        help='Override config transport (e.g. "stdio" or "streamable-http"). '
        "Default: value from config/settings.json.",
    )
    ns = parser.parse_args()
    transport = ns.transport if ns.transport is not None else _CONFIG["transport"]
    mcp.run(transport=transport)
