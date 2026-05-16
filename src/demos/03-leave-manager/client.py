"""Leave Manager MCP client — HTTP (streamable-http) or stdio transport.

**HTTP (default)** — start the server first:

    uv run python src/demos/03-leave-manager/server.py
    uv run python src/demos/03-leave-manager/client.py

**Stdio (one terminal)**:

    uv run python src/demos/03-leave-manager/client.py --stdio
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
       uv run python src/demos/03-leave-manager/server.py
       uv run python src/demos/03-leave-manager/client.py

  2) One terminal — stdio (client starts the server for you):
       uv run python src/demos/03-leave-manager/client.py --stdio
"""


async def demo_session(session: ClientSession) -> None:
    """List tools/resources and run sample async tool calls."""
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
    if not prompts_response.prompts:
        print("  (none in this demo)")
    else:
        for prompt in prompts_response.prompts:
            print(f"  {prompt.name}: {prompt.description}")
    print()

    examples = [
        ("check_leave_balance", {"employee_id": "EMP001"}),
        ("get_database_stats", {}),
        ("get_pending_approvals", {}),
        (
            "submit_leave_request",
            {
                "employee_id": "EMP005",
                "start_date": "2026-06-10",
                "end_date": "2026-06-12",
                "leave_type": "annual",
                "reason": "Team offsite planning",
                "days_requested": 3,
            },
        ),
    ]

    print("Tool calls:")
    for tool_name, args in examples:
        try:
            result = await session.call_tool(tool_name, args)
            text = result.content[0].text if result.content else "(no result)"
            preview = text if len(text) < 320 else text[:320] + "..."
            print(f"  {tool_name} -> {preview}")
        except Exception as exc:
            print(f"  {tool_name} -> ERROR: {exc}")


async def run_http() -> None:
    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await demo_session(session)


async def run_stdio() -> None:
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
        description="Leave Manager MCP demo client (HTTP or stdio).",
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
