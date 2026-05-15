"""Calculator MCP client — HTTP (streamable-http) or stdio transport.

**HTTP (default)** — start the server first, then the client:

    uv run python src/demos/01-calculator/server.py
    uv run python src/demos/01-calculator/client.py

**Stdio (one terminal)** — spawns the server as a subprocess:

    uv run python src/demos/01-calculator/client.py --stdio
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import httpx
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.streamable_http import streamablehttp_client
from settings import load_config

_CONFIG = load_config()
SERVER_URL = f"http://{_CONFIG['host']}:{_CONFIG['port']}/mcp"
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SERVER_SCRIPT = Path(__file__).parent / "server.py"


def _http_connection_help() -> str:
    return f"""Could not reach the MCP server at:
  {SERVER_URL}

Fix (pick one):
  1) Two terminals — start the server, then the client:
       uv run python src/demos/01-calculator/server.py
       uv run python src/demos/01-calculator/client.py

  2) One terminal — stdio (client starts the server for you):
       uv run python src/demos/01-calculator/client.py --stdio
"""


async def demo_session(session: ClientSession) -> None:
    """List tools/resources/prompts and run sample tool calls."""
    await session.initialize()

    tools_response = await session.list_tools()
    print("Available tools:")
    for tool in tools_response.tools:
        print(f"  {tool.name}: {tool.description}")
    print()

    resources_response = await session.list_resources()
    print("Available resources:")
    for resource in resources_response.resources:
        print(f"  {resource.uri}: {resource.description}")
    print()

    prompts_response = await session.list_prompts()
    print("Available prompts:")
    for prompt in prompts_response.prompts:
        print(f"  {prompt.name}: {prompt.description}")
    print()

    examples = [
        ("add", {"a": 10.0, "b": 3.0}),
        ("subtract", {"a": 10.0, "b": 3.0}),
        ("multiply", {"a": 10.0, "b": 3.0}),
        ("divide", {"a": 10.0, "b": 3.0}),
        ("divide", {"a": 10.0, "b": 0.0}),  # expected error
    ]

    print("Tool calls:")
    for tool_name, args in examples:
        try:
            result = await session.call_tool(tool_name, args)
            value = result.content[0].text if result.content else "(no result)"
            print(f"  {tool_name}({args['a']}, {args['b']}) = {value}")
        except Exception as exc:
            print(f"  {tool_name}({args['a']}, {args['b']}) → ERROR: {exc}")


async def run_http() -> None:
    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await demo_session(session)


async def run_stdio() -> None:
    """Spawn server with stdio transport (no separate HTTP server)."""
    params = StdioServerParameters(
        command="uv",
        args=["run", "python", str(_SERVER_SCRIPT), "--transport", "stdio"],
        cwd=str(_REPO_ROOT),
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await demo_session(session)


async def main_async(*, use_stdio: bool) -> None:
    if use_stdio:
        await run_stdio()
    else:
        await run_http()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculator MCP demo client (HTTP or stdio).",
    )
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run against a server subprocess over stdio (no HTTP server needed).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    ns = parse_args()
    try:
        asyncio.run(main_async(use_stdio=ns.stdio))
    except* httpx.ConnectError:
        print(_http_connection_help(), file=sys.stderr)
        raise SystemExit(1) from None
