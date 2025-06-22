from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio

from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Shared tool loader
async def get_tool_runner(tool_filter) -> Runnable:
    """Load MCP tools and filter them based on the provided tool_filter function.
    Returns a Runnable that can invoke the selected tools."""
    
    async with streamablehttp_client("http://localhost:8000/mcp") as (r, w, _):
        async with ClientSession(r, w) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            selected = [t for t in tools if tool_filter(t.name)]
            return llm.bind_tools(selected)
        
        
__all__ = ["get_tool_runner", "llm"]