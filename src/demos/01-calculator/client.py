"""Calculator MCP client — connects to the FastMCP server via streamable-http.

Start the server first:
    python server.py

Then run this client:
    python client.py
"""

import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

SERVER_URL = "http://localhost:8000/mcp"


async def run() -> None:
    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools_response = await session.list_tools()
            print("Available tools:")
            for tool in tools_response.tools:
                print(f"  {tool.name}: {tool.description}")
            print()

            # List available resources
            resources_response = await session.list_resources()
            print("Available resources:")
            for resource in resources_response.resources:
                print(f"  {resource.uri}: {resource.description}")
            print()

            # List available prompts
            prompts_response = await session.list_prompts()
            print("Available prompts:")
            for prompt in prompts_response.prompts:
                print(f"  {prompt.name}: {prompt.description}")
            print()

            # Run example tool calls
            examples = [
                ("add",      {"a": 10.0, "b": 3.0}),
                ("subtract", {"a": 10.0, "b": 3.0}),
                ("multiply", {"a": 10.0, "b": 3.0}),
                ("divide",   {"a": 10.0, "b": 3.0}),
                ("divide",   {"a": 10.0, "b": 0.0}),  # expected error
            ]

            print("Tool calls:")
            for tool_name, args in examples:
                try:
                    result = await session.call_tool(tool_name, args)
                    value = result.content[0].text if result.content else "(no result)"
                    print(f"  {tool_name}({args['a']}, {args['b']}) = {value}")
                except Exception as exc:
                    print(f"  {tool_name}({args['a']}, {args['b']}) → ERROR: {exc}")


if __name__ == "__main__":
    asyncio.run(run())
