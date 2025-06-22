from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio

async def main():
    # Connect to a streamable HTTP server
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            resources = await session.list_resources()
            print(f"Available resources: {resources}")
            
            # Call a tool
            tool_result = await session.call_tool("web_search", {"query": "France travel tips"})
            print(f"Tool result: {tool_result}")
            

if __name__ == "__main__":
    asyncio.run(main())