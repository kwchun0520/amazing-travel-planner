from langchain_core.messages import HumanMessage, SystemMessage
from src.graphs.graph import TravelState
from .tools import llm
import asyncio



async def travel_planner(state: TravelState) -> TravelState:
    """Node to generate a final travel plan based on tour recommendations and expert insights."""
    message = SystemMessage(
        content="You are a travel planner that creates a detailed travel plan based on user preferences and expert insights."
    )
    state["messages"].append(message)
    planner_prompt = HumanMessage(
        content=
        f"""Based on the tour guide suggestions: {state['recommended_places']} and expert insights: {state['expert_insights']},
        generate a travel plan for {state['country']}.
        The user enjoys {state['interests']} and plans to travel for {state['trip_length']} days starting from {state['travel_date']}.
        The user has a budget of {state['budget']} and prefers a travel style of {state['travel_style']}.
        
        Include a day-by-day itinerary, recommended activities, and any necessary travel arrangements.
        Ensure the plan is comprehensive and tailored to the user's preferences.
        Provide the final plan in a clear and structured format.
        Make sure to consider the user's interests, budget, travel style, and the expert insights provided earlier.
        
        Format the response as a detailed travel plan with headings for each day and activities as well ways to commute to the place/activities such as public transport, taxi, or walking.
        Please also include any travel incidents, weather conditions, accommodation options, and flight details relevant to the trip.
        
        For example:
        Day 1: Arrival in [City]
        - Activity 1: [Description]
        - Activity 2: [Description]
        ...
        Day 2: [City]
        - Activity 1: [Description]
        - Activity 2: [Description]
        ...
        
        - Travel Incidents/details: [details]
        - Weather: [current weather conditions]
        - Accommodation: [hotel recommendations]
        - Flights: [flight options]
        
        - Include any necessary travel arrangements, such as transportation and accommodation.
        - Ensure to include the user's interests and travel date in your response.

       
        Continue this format for the entire trip length.
        Ensure to include any necessary travel arrangements, such as transportation and accommodation.
        Provide the final plan as a single response without any additional commentary.
        """
    )
    state["messages"].append(planner_prompt)
    result = await llm.ainvoke(state["messages"])
    return {"final_plan": result.content}


__all__ = ["travel_planner"]