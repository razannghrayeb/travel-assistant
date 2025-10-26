"""
Travel Crew Setup
Configures the CrewAI crew with agents and tasks
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from crewai import Crew, Process

# Load environment variables
load_dotenv()

# Import agents and tasks
from agents import flight_agent, hotel_agent, tour_agent, advice_agent
from tasks import task_flights, task_hotels, task_tour, task_advice

def travel_crew_setup():
    """
    Setup the travel crew with agents and tasks.
    
    Returns:
        Crew: Configured CrewAI crew ready to execute travel planning
    """
    # Create and return the Crew instance
    return Crew(
        agents=[flight_agent, hotel_agent, tour_agent, advice_agent],
        tasks=[task_flights, task_hotels, task_tour, task_advice],
        process=Process.sequential,
        verbose=True
    )
