"""Advice Task - Provide travel advice"""

from crewai import Task
from agents.advice_agent import advice_agent

task_advice = Task(
    description=(
        "Give travel advice for {destination}. "
        "Use the give_advice tool with destination='{destination}'. "
        "Provide practical safety tips, cultural etiquette, "
        "and important local customs travelers should be aware of."
    ),
    expected_output=(
        "Travel safety and cultural tips for {destination}, including "
        "important customs, safety precautions, and local etiquette."
    ),
    agent=advice_agent
)
