import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from crewai.tools import tool
from tools.gemini import gemini_generate

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

@tool
def check_hotels(destination: str, checkin_date: str = None, checkout_date: str = None):
    """Fetch hotel data using Booking.com API (via RapidAPI - booking-com15).
    Args:
        destination: City name
        checkin_date: Check-in date in YYYY-MM-DD format
        checkout_date: Check-out date in YYYY-MM-DD format
    """
    # Set default dates if not provided
    if not checkin_date:
        checkin_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not checkout_date:
        checkout_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "booking-com15.p.rapidapi.com"
    }
    
    try:
        # Step 1: Search for destination
        search_url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
        search_params = {"query": destination}
        
        search_response = requests.get(search_url, headers=headers, params=search_params, timeout=10)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        if not search_data.get("data") or len(search_data["data"]) == 0:
            # Fallback to Gemini if no destination found
            prompt = f"List 5 recommended hotels in {destination} with ratings and approximate prices for dates {checkin_date} to {checkout_date}."
            return gemini_generate(prompt)
        
        # Get the first destination result
        dest_id = search_data["data"][0].get("dest_id")
        dest_name = search_data["data"][0].get("search_type", destination)
        
        # Step 2: Search for hotels
        hotels_url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
        hotels_params = {
            "dest_id": dest_id,
            "search_type": "CITY",
            "arrival_date": checkin_date,
            "departure_date": checkout_date,
            "adults": "1",
            "room_qty": "1",
            "page_number": "1",
            "units": "metric",
            "temperature_unit": "c",
            "languagecode": "en-us",
            "currency_code": "USD"
        }
        
        hotels_response = requests.get(hotels_url, headers=headers, params=hotels_params, timeout=15)
        hotels_response.raise_for_status()
        hotels_data = hotels_response.json()
        
        if not hotels_data.get("data") or not hotels_data["data"].get("hotels"):
            # Fallback to Gemini if no hotels found
            prompt = f"List 5 recommended hotels in {destination} with ratings and approximate prices for dates {checkin_date} to {checkout_date}."
            return gemini_generate(prompt)
        
        hotels = []
        hotel_list = hotels_data["data"]["hotels"][:5]  # Get top 5 hotels
        
        for h in hotel_list:
            name = h.get("property", {}).get("name", "Unknown Hotel")
            rating = h.get("property", {}).get("reviewScore", "N/A")
            review_word = h.get("property", {}).get("reviewScoreWord", "")
            price_info = h.get("property", {}).get("priceBreakdown", {})
            gross_price = price_info.get("grossPrice", {}).get("value", "N/A")
            currency = price_info.get("grossPrice", {}).get("currency", "USD")
            
            hotel_info = f"{name}"
            if rating != "N/A":
                hotel_info += f" - {rating}/10 ({review_word})"
            hotel_info += f"\nPrice: {gross_price} {currency}"
            
            hotels.append(hotel_info)
        
        return f"Top hotels in {dest_name} (Check-in: {checkin_date}, Check-out: {checkout_date}):\n\n" + "\n---\n".join(hotels)
        
    except requests.exceptions.RequestException as e:
        # Fallback to Gemini on any API error
        try:
            prompt = f"List 5 recommended hotels in {destination} with ratings and approximate prices for dates {checkin_date} to {checkout_date}. Format nicely."
            return gemini_generate(prompt)
        except:
            return f"Error fetching hotels: {e}"
    except Exception as e:
        # Fallback to Gemini on any error
        try:
            prompt = f"List 5 recommended hotels in {destination} with ratings and approximate prices for dates {checkin_date} to {checkout_date}."
            return gemini_generate(prompt)
        except:
            return f"Error fetching hotels: {e}"
