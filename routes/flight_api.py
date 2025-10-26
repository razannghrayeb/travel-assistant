from fastapi import APIRouter, Query
from crewai import Crew
from datetime import datetime, timedelta
from agents.flight_agent import flight_agent
from tasks.flight_task import task_flights

router = APIRouter(prefix="/flights", tags=["Flights"])

@router.get("/")
def get_flights(destination: str, flight_date: str = Query(None)):
    """
    Get flight information for a specific destination and optional date using CrewAI agent.
    
    Args:
        destination: Airport IATA code or city name (e.g., 'JFK', 'LAX', 'DXB', 'Beirut')
        flight_date: Flight date in YYYY-MM-DD format (optional, default: tomorrow)
    
    Returns:
        Flight information as text
    """
    # Set default date if not provided
    if not flight_date:
        flight_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Create a crew with just the flight agent and task
    flight_crew = Crew(
        agents=[flight_agent],
        tasks=[task_flights],
        verbose=True
    )
    
    # Execute the crew
    result = flight_crew.kickoff(inputs={
        "destination": destination,
        "flight_date": flight_date
    })
    
    return {
        "destination": destination, 
        "flight_date": flight_date, 
        "data": str(result)
    }