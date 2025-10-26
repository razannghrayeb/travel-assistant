import os
import requests
from crewai.tools import tool
from tools.gemini import gemini_generate

GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")

@tool
def prepare_tour(destination: str):
    """List top attractions using Google Places API - Find Place endpoint."""
    try:
        # Use the Find Place API endpoint (not the legacy places method)
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": f"tourist attractions in {destination}",
            "inputtype": "textquery",
            "fields": "name,formatted_address,rating",
            "key": GOOGLE_MAPS_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "OK":
            # Fallback: Use Gemini to generate attractions
            prompt = f"List 5 top tourist attractions in {destination} with brief descriptions."
            return gemini_generate(prompt)
        
        candidates = data.get("candidates", [])[:5]
        if not candidates:
            return f"No tourist attractions found for {destination}."
        
        attractions = []
        for place in candidates:
            name = place.get("name", "Unknown")
            rating = place.get("rating", "N/A")
            address = place.get("formatted_address", "No address")
            attractions.append(f"{name} (Rating: {rating})\n{address}")
        
        return "Top attractions in " + destination + ":\n\n" + "\n---\n".join(attractions)
    except Exception as e:
        # Fallback to Gemini if API fails
        try:
            prompt = f"List 5 top must-see tourist attractions in {destination} with brief descriptions."
            return gemini_generate(prompt)
        except:
            return f"Error fetching attractions: {e}"
