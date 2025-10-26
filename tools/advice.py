import os
from dotenv import load_dotenv
from crewai.tools import tool
from tools.gemini import gemini_generate

@tool
def give_advice(destination: str):
    """Generate travel advice via Gemini."""
    prompt = f"Give 3 important travel safety and cultural tips for visiting {destination}."
    return gemini_generate(prompt)