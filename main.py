"""
Travel Assistant Main Application
Orchestrates agents and tasks for comprehensive travel planning
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables for LiteLLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# Import crew setup
from crew import travel_crew_setup

# =========================
# MAIN FUNCTION
# =========================

def run_travel_assistant(destination, flight_date=None, checkin_date=None, checkout_date=None):
    """
    Run the travel assistant with dates.
    
    Args:
        destination: Destination city or airport code
        flight_date: Flight date in YYYY-MM-DD format (default: tomorrow)
        checkin_date: Hotel check-in date in YYYY-MM-DD format (default: tomorrow)
        checkout_date: Hotel check-out date in YYYY-MM-DD format (default: 2 days after check-in)
    
    Returns:
        Travel plan with flights, hotels, attractions, and advice
    """
    # Set default dates if not provided
    if not flight_date:
        flight_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not checkin_date:
        checkin_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not checkout_date:
        checkin_dt = datetime.strptime(checkin_date, "%Y-%m-%d")
        checkout_date = (checkin_dt + timedelta(days=2)).strftime("%Y-%m-%d")
    
    print(f"\n🌍 Planning your trip to {destination}...")
    print(f"📅 Flight Date: {flight_date}")
    print(f"🏨 Hotel: {checkin_date} to {checkout_date}\n")
    
    # Setup and run the crew
    travel_crew = travel_crew_setup()
    
    result = travel_crew.kickoff(inputs={
        "destination": destination,
        "flight_date": flight_date,
        "checkin_date": checkin_date,
        "checkout_date": checkout_date
    })
    
    print("\n===== FINAL TRAVEL PLAN =====\n")
    print(result)
    
    return result

# =========================
# CLI INTERFACE
# =========================

if __name__ == "__main__":
    print("=" * 60)
    print("🌍 WELCOME TO TRAVEL ASSISTANT 🌍")
    print("=" * 60)
    
    dest = input("\nEnter your travel destination (city or airport code): ")
    
    # Ask for dates
    print("\nEnter dates (press Enter to use defaults):")
    flight_date = input("Flight date (YYYY-MM-DD, default: tomorrow): ").strip()
    checkin_date = input("Hotel check-in date (YYYY-MM-DD, default: tomorrow): ").strip()
    checkout_date = input("Hotel check-out date (YYYY-MM-DD, default: 2 days after check-in): ").strip()
    
    # Convert empty strings to None
    flight_date = flight_date if flight_date else None
    checkin_date = checkin_date if checkin_date else None
    checkout_date = checkout_date if checkout_date else None
    
    # Run the travel assistant
    run_travel_assistant(dest, flight_date, checkin_date, checkout_date)
