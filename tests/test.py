import pytest
import asyncio
from src.graphs.runner import run_planner

@pytest.mark.asyncio
async def test_run_planner():
    interests = "history, culture, food"
    country = "Japan"
    trip_length = 10
    budget = "moderate"
    travel_style = "cultural immersion"
    travel_date = "2024-01-01"

    result = await run_planner(
        interests=interests,
        country=country,
        trip_length=trip_length,
        budget=budget,
        travel_style=travel_style,
        travel_date=travel_date
    )
    assert result is not None
    assert isinstance(result, str)