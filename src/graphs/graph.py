from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from .state import TravelState
from src.agents import tour_guide, travel_expert, travel_planner


def build_graph() -> CompiledStateGraph:
    """Build the travel planning graph with nodes for tour guide, expert, and planner."""
    
    graph = StateGraph(TravelState)
    graph.add_node("TourGuide", tour_guide)
    graph.add_node("Expert", travel_expert)
    graph.add_node("Planner", travel_planner)

    graph.set_entry_point("TourGuide")
    graph.add_edge("TourGuide", "Expert")
    graph.add_edge("Expert", "Planner")
    graph.add_edge("Planner", END)

    return graph.compile()

agent_graph = build_graph()


__all__ = ["agent_graph"]