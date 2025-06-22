from langchain_core.messages import HumanMessage, SystemMessage
from src.graphs.graph import TravelState
from .tools import get_tool_runner
import asyncio


async def travel_expert(state: TravelState) -> TravelState:
    """Node to gather expert insights on travel incidents, weather, accommodation, and flights."""
    runner = await get_tool_runner(lambda name: name in {
        "check_travel_incidents", "get_weather", "find_hotels", "search_flights"
    })
    system_message = SystemMessage(
        content="""You are a travel expert that provides insights on travel incidents, weather, accommodation, and flights.
        Use the user's country and travel date to provide relevant information.
        Ensure to include details about travel incidents, current weather, accommodation options, and flight availability.
        Provide a comprehensive overview that helps the user plan their trip effectively.
        Use the following format for your response:
        - Travel Incidents: [details]
        - Weather: [current weather conditions]
        - Accommodation: [hotel recommendations]
        - Flights: [flight options]
        Make sure to include the user's interests and travel date in your response.
        """
    )
    state["messages"].append(system_message)
    prompt = HumanMessage(content=
        f"Tell me about travel incidents, weather, accommodation, and flights for {state['country']} in relations to {state["recommended_places"]} on {state['travel_date']}. User plans to travel for {state['trip_length']} days"
    )
    state["messages"].append(prompt)
    result = await runner.ainvoke(state["messages"])
    return {"expert_insights": result.content}

__all__ = ["travel_expert"]