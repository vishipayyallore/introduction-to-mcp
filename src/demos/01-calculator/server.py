"""Calculator MCP server — FastMCP edition.

Run with streamable-http (default, serves on http://localhost:8000/mcp):
    python server.py

Inspect interactively with the MCP CLI:
    mcp dev server.py
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calculator", json_response=True)


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
    """Prompt the model to evaluate a mathematical expression using the calculator tools."""
    return (
        f"Evaluate the following expression using only the available calculator tools "
        f"(add, subtract, multiply, divide): {expression}"
    )


# --- Entry point -------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
