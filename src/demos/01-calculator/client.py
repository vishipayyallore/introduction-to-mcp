"""MCP calculator client — launches the server and calls each tool in sequence."""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER = Path(__file__).parent / "server.py"


async def run() -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER)],
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools_response = await session.list_tools()
            print("Available tools:")
            for tool in tools_response.tools:
                print(f"  {tool.name}: {tool.description}")
            print()

            # Run a set of example calls
            examples = [
                ("add",      {"a": 10,  "b": 3}),
                ("subtract", {"a": 10,  "b": 3}),
                ("multiply", {"a": 10,  "b": 3}),
                ("divide",   {"a": 10,  "b": 3}),
                ("divide",   {"a": 10,  "b": 0}),  # expected error
            ]

            for tool_name, args in examples:
                try:
                    result = await session.call_tool(tool_name, args)
                    value = result.content[0].text if result.content else "(no result)"
                    print(f"{tool_name}({args['a']}, {args['b']}) = {value}")
                except Exception as exc:
                    print(f"{tool_name}({args['a']}, {args['b']}) → ERROR: {exc}")


if __name__ == "__main__":
    asyncio.run(run())
