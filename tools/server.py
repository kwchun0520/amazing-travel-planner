from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from langchain_community.tools import DuckDuckGoSearchResults


# Create an MCP server
mcp = FastMCP(
    name ="travel_planner",
    # host="0.0.0.0",
    # port=8000,
    stateless_http=False, 
    json_response=True
)

search_tool = DuckDuckGoSearchResults(num_results=3)

# @mcp.prompt()
# def travel_planner_prompt(
#     country: str, 
#     travel_date: str, 
#     hobbies: str, 
#     travel_style: str
# ) -> str:
#     """
#     Generate a travel plan based on user inputs.

#     Args:
#         country (str): The country to visit.
#         travel_date (str): The date of travel.
#         hobbies (str): User's hobbies.
#         travel_style (str): User's preferred travel style.

#     Returns:
#         str: A personalized travel plan.
#     """
#     return (
#         f"Plan a trip to {country} on {travel_date}. "
#         f"Include activities related to {hobbies} and consider a {travel_style} style."
#     )

# @mcp.tool()
# def generate_travel_plan(
#     country: str, 
#     travel_date: str, 
#     hobbies: str, 
#     travel_style: str
# ) -> str:
#     """
#     Generate a travel plan based on user inputs.

#     Args:
#         country (str): The country to visit.
#         travel_date (str): The date of travel.
#         hobbies (str): User's hobbies.
#         travel_style (str): User's preferred travel style.

#     Returns:
#         str: A personalized travel plan.
#     """
#     prompt = travel_planner_prompt(country, travel_date, hobbies, travel_style)
    
#     # Here you would typically call an LLM or another service to generate the plan
#     # For simplicity, we will just return the prompt as the "plan"
#     return f"Generated Travel Plan: {prompt}"


# # Add an addition tool
# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers"""
#     return a + b


# # Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"


# @mcp.tool()
# def search_web(query: str) -> str:
#     """
#     Searches the web using DuckDuckGo and returns results.

#     Args:
#         query (str): The search query.

#     Returns:
#         str: Search results from DuckDuckGo.
#     """
#     return DuckDuckGoSearchResults(num_results=5).run(query)


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