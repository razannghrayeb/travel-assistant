"""Hotel Task - Find hotel accommodations"""

from crewai import Task
from agents.hotel_agent import hotel_agent

task_hotels = Task(
    description=(
        "Find hotel recommendations in {destination} for check-in on {checkin_date} "
        "and check-out on {checkout_date}. "
        "Use the check_hotels tool with destination='{destination}', "
        "checkin_date='{checkin_date}', and checkout_date='{checkout_date}'. "
        "Include ratings, prices, and amenities for each hotel."
    ),
    expected_output=(
        "Hotel list for {destination} with ratings, prices, and key amenities "
        "for the specified dates ({checkin_date} to {checkout_date})."
    ),
    agent=hotel_agent
)
