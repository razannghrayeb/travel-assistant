"""Tour Agent - Specialized in planning tourist itineraries"""

from crewai import Agent
from tools.google_place import prepare_tour

# LLM model configuration
llm_model = "gemini/gemini-2.5-flash"

tour_agent = Agent(
    role="Tour Planner",
    goal="Design travel itineraries with must-see attractions in {destination}.",
    backstory="An enthusiastic guide who crafts amazing tourism plans. "
              "I've visited countless destinations and know all the hidden gems "
              "and must-see attractions that make trips unforgettable.",
    tools=[prepare_tour],
    llm=llm_model,
    verbose=True
)
