from typing import TypedDict, Optional, Sequence, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


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
    
    

__all__ = ["TravelState"]