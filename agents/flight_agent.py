"""Flight Agent - Specialized in finding flight options"""

from crewai import Agent
from tools.check_flights import check_flights

# LLM model configuration
llm_model = "gemini/gemini-2.5-flash"

flight_agent = Agent(
    role="Flight Finder",
    goal="Provide travelers with flight options for {destination} on {flight_date}.",
    backstory="An expert travel agent specialized in global flight search. "
              "I have years of experience finding the best flight options "
              "for travelers around the world.",
    tools=[check_flights],
    llm=llm_model,
    verbose=True
)
