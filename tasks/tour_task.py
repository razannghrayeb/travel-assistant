"""Tour Task - Plan tourist attractions"""

from crewai import Task
from agents.tour_agent import tour_agent

task_tour = Task(
    description=(
        "List top tourist attractions in {destination}. "
        "Use the prepare_tour tool with destination='{destination}'. "
        "Provide detailed information about each attraction including "
        "ratings, addresses, and why they're worth visiting."
    ),
    expected_output=(
        "List of top attractions in {destination} with ratings, "
        "addresses, and descriptions of what makes each place special."
    ),
    agent=tour_agent
)
