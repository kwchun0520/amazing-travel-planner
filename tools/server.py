from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from langchain_community.tools import DuckDuckGoSearchResults


# Create an MCP server
mcp = FastMCP(
    name ="travel_planner",
    host="0.0.0.0",
    port=8000,
    stateless_http=False, 
    json_response=True
)

search_tool = DuckDuckGoSearchResults(num_results=3)

@mcp.tool()
def recommend_places(hobby: str, country: str) -> str:
    """Return tourist attractions in a country based on user's hobby."""
    query = f"top tourist attractions in {country} for {hobby} lovers"
    return search_tool.run(query)

@mcp.tool()
def check_travel_incidents(destination: str) -> str:
    """Returns recent travel incidents in the destination."""
    query = f"recent travel safety incidents in {destination}"
    return search_tool.run(query)

@mcp.tool()
def get_weather(destination: str) -> str:
    """Returns current weather."""
    query = f"current weather in {destination}"
    return search_tool.run(query)

@mcp.tool()
def find_hotels(destination: str) -> str:
    """Find hotel recommendations."""
    query = f"best hotels in {destination}"
    return search_tool.run(query)

@mcp.tool()
def search_flights(destination: str) -> str:
    """Returns flight options."""
    query = f"flight options to {destination}"
    return search_tool.run(query)

@mcp.tool()
def web_search(query: str) -> str:
    """
    Perform a web search using DuckDuckGo and return the results.
    """
    return search_tool.run(query)




if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="streamable-http")