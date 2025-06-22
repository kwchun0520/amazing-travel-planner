from langchain_core.messages import HumanMessage
from .graph import agent_graph
from .state import TravelState

async def run_planner(interests: str, country: str, trip_length: int = 7,
                      budget: str = "moderate", travel_style: str = "chilling",
                      travel_date: str = "2024-01-01") -> str:
    """Run the travel planner with the given parameters."""
    initial_state = TravelState(
        country=country,
        interests=interests,
        trip_length=trip_length,
        budget=budget,
        travel_style=travel_style,
        travel_date=travel_date,
        messages=[HumanMessage(content=f"Plan a trip to {country} for {trip_length} days with a budget of {budget}.")]
    )

    result = await agent_graph.ainvoke(initial_state)
    return result["final_plan"]


__all__ = ["run_planner"]