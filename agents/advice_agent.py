"""Advice Agent - Specialized in providing travel advice"""

from crewai import Agent
from tools.advice import give_advice

# LLM model configuration
# Using gemini-2.5-flash as it's stable and available
# LLM model configuration
llm_model = "gemini/gemini-2.5-flash"

advice_agent = Agent(
    role="Travel Advisor",
    goal="Give cultural and safety tips for {destination}.",
    backstory="A seasoned travel blogger offering advice worldwide. "
              "I've traveled to hundreds of countries and understand "
              "local customs, safety protocols, and cultural nuances.",
    tools=[give_advice],
    llm=llm_model,
    verbose=True
)
