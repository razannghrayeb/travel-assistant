from fastapi import APIRouter, Query
from crewai import Crew
from datetime import datetime, timedelta
from agents.hotel_agent import hotel_agent
from tasks.hotel_task import task_hotels

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("/")
def get_hotels(destination: str, checkin_date: str = Query(None), checkout_date: str = Query(None)):
    """
    Get hotel recommendations for a specific destination and date range using CrewAI agent.
    
    Args:
        destination: City name
        checkin_date: Check-in date in YYYY-MM-DD format (optional, default: tomorrow)
        checkout_date: Check-out date in YYYY-MM-DD format (optional, default: 2 days after check-in)
    
    Returns:
        Hotel recommendations with ratings and prices
    """
    # Set default dates if not provided
    if not checkin_date:
        checkin_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not checkout_date:
        checkin_dt = datetime.strptime(checkin_date, "%Y-%m-%d")
        checkout_date = (checkin_dt + timedelta(days=2)).strftime("%Y-%m-%d")
    
    # Create a crew with just the hotel agent and task
    hotel_crew = Crew(
        agents=[hotel_agent],
        tasks=[task_hotels],
        verbose=True
    )
    
    # Execute the crew
    result = hotel_crew.kickoff(inputs={
        "destination": destination,
        "checkin_date": checkin_date,
        "checkout_date": checkout_date
    })
    
    return {
        "destination": destination, 
        "checkin_date": checkin_date,
        "checkout_date": checkout_date,
        "data": str(result)
    }
