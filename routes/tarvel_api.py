from fastapi import APIRouter, Query
from crewai import Crew
from agents.tour_agent import tour_agent
from tasks.tour_task import task_tour

router = APIRouter(prefix="/tour", tags=["Tourism"])

@router.get("/")
def get_tour(destination: str = Query(...)):
    """
    Get top tourist attractions for a destination using CrewAI agent.
    
    Args:
        destination: City or destination name
    
    Returns:
        List of top tourist attractions with ratings and addresses
    """
    # Create a crew with just the tour agent and task
    tour_crew = Crew(
        agents=[tour_agent],
        tasks=[task_tour],
        verbose=True
    )
    
    # Execute the crew
    result = tour_crew.kickoff(inputs={
        "destination": destination
    })
    
    return {
        "destination": destination, 
        "data": str(result)
    }