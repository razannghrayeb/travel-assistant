from fastapi import APIRouter, Query
from crewai import Crew
from agents.advice_agent import advice_agent
from tasks.advice_task import task_advice

router = APIRouter(prefix="/advice", tags=["Advice"])

@router.get("/")
def get_travel_advice(destination: str = Query(...)):
    """
    Get travel advice for a specific destination using CrewAI agent.
    
    Args:
        destination: City or destination name
    
    Returns:
        Travel safety and cultural tips
    """
    # Create a crew with just the advice agent and task
    advice_crew = Crew(
        agents=[advice_agent],
        tasks=[task_advice],
        verbose=True
    )
    
    # Execute the crew
    result = advice_crew.kickoff(inputs={
        "destination": destination
    })
    
    return {
        "destination": destination, 
        "data": str(result)
    }
