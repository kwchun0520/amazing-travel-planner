from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchResults
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent





model = OllamaLLM(
    model="llama3.2",
    base_url="http://localhost:11434"
)

@tool
def search_web_tool(query: str) -> str:
    """
    Searches the web using DuckDuckGo and returns results.

    Args:
        query (str): The search query.

    Returns:
        str: Search results from DuckDuckGo.
    """
    search_tool = DuckDuckGoSearchResults(num_results=10, verbose=True)
    return search_tool.run(query)