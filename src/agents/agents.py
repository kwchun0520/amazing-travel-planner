from langgraph.graph import StateGraph, END
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

from typing import TypedDict, Optional, Sequence, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

class TravelState(TypedDict, total=False):
    country: str
    interests: str
    trip_length: Optional[int]  # in days
    budget: str
    travel_style: str
    travel_date: str  # date of travel
    recommended_places: Optional[str]
    expert_insights: Optional[str]
    final_plan: Optional[str]
    messages: Annotated[Sequence[BaseMessage],add_messages]
    

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

# Nodes
async def tour_guide_node(state: TravelState) -> TravelState:
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

async def expert_node(state: TravelState) -> TravelState:
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

async def planner_node(state: TravelState) -> TravelState:
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

# LangGraph assembly
def build_graph():
    builder = StateGraph(TravelState)
    builder.add_node("TourGuide", tour_guide_node)
    builder.add_node("Expert", expert_node)
    builder.add_node("Planner", planner_node)

    builder.set_entry_point("TourGuide")
    builder.add_edge("TourGuide", "Expert")
    builder.add_edge("Expert", "Planner")
    builder.add_edge("Planner", END)

    return builder.compile()

graph = build_graph()

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

    result = await graph.ainvoke(initial_state)
    return result["final_plan"]


__all__ = ["run_planner", "graph"]