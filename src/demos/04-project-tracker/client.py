"""Project Tracker MCP client - HTTP (streamable-http) or stdio transport.

**HTTP (default)** - start the server first:

    uv run python src/demos/04-project-tracker/server.py
    uv run python src/demos/04-project-tracker/client.py

**Stdio (one terminal)**:

    uv run python src/demos/04-project-tracker/client.py --stdio
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import httpx
from mcp import ClientSession
from pydantic import AnyUrl
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
  1) Two terminals - start the server, then the client:
       uv run python src/demos/04-project-tracker/server.py
       uv run python src/demos/04-project-tracker/client.py

  2) One terminal - stdio (client starts the server for you):
       uv run python src/demos/04-project-tracker/client.py --stdio
"""


async def demo_session(session: ClientSession) -> None:
    """List tools/resources/templates and run sample calls."""
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

    tmpl_response = await session.list_resource_templates()
    print("Resource templates:")
    for tmpl in tmpl_response.resourceTemplates:
        print(f"  {tmpl.uriTemplate}: {tmpl.description}")
    print()

    prompts_response = await session.list_prompts()
    print("Available prompts:")
    if not prompts_response.prompts:
        print("  (none in this demo)")
    else:
        for prompt in prompts_response.prompts:
            print(f"  {prompt.name}: {prompt.description}")
    print()

    print("Sample reads (stateful DB snapshots):")
    for uri in ("ticket://TK002", "tickets://for-project/PROJ002", "project://PROJ001"):
        try:
            rr = await session.read_resource(AnyUrl(uri))
            block = rr.contents[0].text if rr.contents else "(empty)"
            preview = block if len(block) < 400 else block[:400] + "..."
            print(f"  read_resource({uri}) ->\n{preview}\n")
        except Exception as exc:
            print(f"  read_resource({uri}) -> ERROR: {exc}\n")

    examples = [
        (
            "update_ticket_status",
            {"ticket_id": "TK004", "new_status": "in_progress", "updater": "MCP Client Demo"},
        ),
        (
            "create_ticket",
            {
                "title": "Docs: MCP resource URIs",
                "description": "Document ticket:// and tickets://for-project patterns.",
                "priority": "low",
                "assignee": "Nick Chen",
                "reporter": "Sarah Davis",
                "project": "API Integration",
                "due_date": "",
                "tags": "docs,mcp",
            },
        ),
    ]

    print("Tool calls:")
    for tool_name, args in examples:
        try:
            result = await session.call_tool(tool_name, args)
            text = result.content[0].text if result.content else "(no result)"
            preview = text if len(text) < 400 else text[:400] + "..."
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
        description="Project Tracker MCP demo client (HTTP or stdio).",
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
