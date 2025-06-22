from langchain_core.messages import HumanMessage, SystemMessage
from src.graphs.graph import TravelState
from .tools import get_tool_runner
import asyncio


# Nodes
async def tour_guide(state: TravelState) -> TravelState:
    """Node to recommend tourist attractions based on user's hobby."""
    runner = await get_tool_runner(lambda name: "recommend_places" in name)
    system_message = SystemMessage(
        content="""You are a travel guide that recommends tourist attractions based on user interests.
        Use the user's interests and country to provide relevant recommendations.
        Ensure to include a variety of places such as historical sites, natural wonders, and cultural experiences.
        Provide a comprehensive list of recommended places that align with the user's interests.
        Use the following format for your response:
        - Place 1: [description]
        - Place 2: [description]
        - Place 3: [description]
        Make sure to include the user's interests and country in your response.
        Make sure to include the way to commute to the place, such as public transport, taxi, or walking.
        Provide the recommendations in a single response without any additional commentary.
        """
    )
    prompt = HumanMessage(content=f"User enjoys {state['interests']}. Recommend places in {state['country']}")
    state["messages"].append(system_message)
    state["messages"].append(prompt)
    # Invoke the tool to get recommendations
    result = await runner.ainvoke(state["messages"])
    
    return {"recommended_places": result.content}


__all__ = ["tour_guide"]