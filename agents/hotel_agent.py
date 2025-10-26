"""Hotel Agent - Specialized in finding hotel accommodations"""

from crewai import Agent
from tools.check_hotels import check_hotels

# LLM model configuration
llm_model = "gemini/gemini-2.5-flash"

hotel_agent = Agent(
    role="Hotel Recommender",
    goal="Suggest comfortable hotels at good prices in {destination} for check-in on {checkin_date} and check-out on {checkout_date}.",
    backstory="A hospitality expert who knows the best hotels in every city. "
              "I have insider knowledge of accommodations worldwide and "
              "can find the perfect stay for any budget.",
    tools=[check_hotels],
    llm=llm_model,
    verbose=True
)
