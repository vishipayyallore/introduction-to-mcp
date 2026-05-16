"""Calculator MCP server — FastMCP edition.

HTTP mode (default — serves on http://127.0.0.1:8000/mcp):
    uv run python src/demos/01-calculator/server.py

Stdio mode (for subprocess clients or the MCP Inspector):
    uv run python src/demos/01-calculator/server.py --transport stdio
"""

from mcp.server.fastmcp import FastMCP
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


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a and return the result."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the result."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b. Raises an error if b is zero."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


# --- Resources ---------------------------------------------------------------


@mcp.resource("calculation://help")
def calculation_help() -> str:
    """Reference guide for the available calculator tools."""
    return (
        "Available operations: add, subtract, multiply, divide.\n"
        "All tools accept two float arguments (a, b) and return a float.\n"
        "divide(a, 0) raises an error."
    )


# --- Prompts -----------------------------------------------------------------


@mcp.prompt()
def evaluate(expression: str) -> str:
    """Prompt the model to evaluate an expression with calculator tools."""
    return (
        f"Evaluate the following expression using only the available calculator tools "
        f"(add, subtract, multiply, divide): {expression}"
    )


# --- Entry point -------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Calculator MCP server (FastMCP).")
    parser.add_argument(
        "--transport",
        default=None,
        metavar="NAME",
        help='Override config transport (e.g. "stdio" for subprocess clients, '
        '"streamable-http" for HTTP). Default: value from config/settings.json.',
    )
    ns = parser.parse_args()
    transport = ns.transport if ns.transport is not None else _CONFIG["transport"]
    mcp.run(transport=transport)
