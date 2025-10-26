"""Flight Task - Find available flights"""

from crewai import Task
from agents.flight_agent import flight_agent

task_flights = Task(
    description=(
        "Find available flights to {destination} on {flight_date}. "
        "Use the check_flights tool with destination='{destination}' "
        "and flight_date='{flight_date}'. "
        "Provide comprehensive flight information including airlines, "
        "flight numbers, departure/arrival times, and status."
    ),
    expected_output=(
        "List of flights to {destination} on {flight_date} with airline, "
        "departure/arrival times, flight numbers, and current status."
    ),
    agent=flight_agent
)
