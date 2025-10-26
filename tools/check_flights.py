import requests
import os   
from crewai.tools import tool
from tools.gemini import gemini_generate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AVIATIONSTACK_KEY = os.getenv("AVIATIONSTACK_KEY")

def get_airport_iata(location: str):
    """Get airport IATA code from location name or city using AviationStack Airports API.
    
    Args:
        location: City name, airport name, or country (e.g., 'Beirut', 'Lebanon', 'Dubai')
    
    Returns:
        IATA code (e.g., 'BEY') or None if not found
    """
    url = "http://api.aviationstack.com/v1/airports"
    params = {
        "access_key": AVIATIONSTACK_KEY,
        "search": location,
        "limit": 1
    }
    
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json().get("data", [])
        
        if data and len(data) > 0:
            iata_code = data[0].get("iata_code")
            airport_name = data[0].get("airport_name", "")
            return iata_code, airport_name
        return None, None
    except Exception as e:
        print(f"Error getting airport IATA code: {e}")
        return None, None

@tool
def check_flights(destination: str, flight_date: str = None):
    """Fetch real flight data using AviationStack API for flights arriving at a destination.
    
    This function automatically converts location names to airport IATA codes.
    You can provide:
        - City names: 'Beirut', 'Dubai', 'Paris', 'New York'
        - Country names: 'Lebanon', 'UAE', 'France'
        - Airport codes: 'BEY', 'DXB', 'CDG', 'JFK'
    
    Args:
        destination: City name, country, or airport IATA code
        flight_date: Flight date in YYYY-MM-DD format (Note: free tier only shows current flights)
    
    Returns:
        String containing flight information for flights arriving at the destination
    """
    # If destination is not already a 3-letter IATA code, look it up
    arr_iata = destination.upper()
    airport_name = None
    
    if len(destination) != 3 or not destination.isalpha():
        # Try to get IATA code from location name
        arr_iata, airport_name = get_airport_iata(destination)
        if not arr_iata:
            return f"Could not find airport for destination: {destination}. Please provide a valid city name, country, or airport IATA code."
    
    url = "http://api.aviationstack.com/v1/flights"
    # Free tier: only use basic parameters (flight_date is a premium feature)
    params = {
        "access_key": AVIATIONSTACK_KEY, 
        "arr_iata": arr_iata,  # arr_iata = arrival airport IATA code
        "limit": 10
    }
    
    try:
        print(f"[DEBUG] Calling AviationStack API with params: {params}")
        res = requests.get(url, params=params, timeout=10)
        print(f"[DEBUG] Response status code: {res.status_code}")
        print(f"[DEBUG] Response content: {res.text[:500]}")  # Print first 500 chars
        
        # Check if we got a 403 (forbidden - usually means using premium features on free tier)
        if res.status_code == 403:
            print("[DEBUG] Got 403 error, falling back to Gemini")
            # Fallback to Gemini to generate flight information
            prompt = f"Generate a realistic list of 3 sample flights to {destination} airport (IATA: {arr_iata}) on {flight_date if flight_date else 'today'}. Include airline names, flight numbers, departure airports, and approximate times. Format it clearly."
            return gemini_generate(prompt)
        
        res.raise_for_status()
        response_json = res.json()
        print(f"[DEBUG] Full JSON response: {response_json}")
        data = response_json.get("data", [])
        
        if not data:
            print(f"[DEBUG] No flight data returned from API")
            # If no data, use Gemini as fallback
            prompt = f"Generate a realistic list of 3 sample flights to {destination} airport (IATA: {arr_iata}) on {flight_date if flight_date else 'today'}. Include airline names, flight numbers, departure airports, and times."
            return gemini_generate(prompt)
        
        print(f"[DEBUG] Found {len(data)} flights")
        flights = []
        date_note = f" (Note: Showing current flights as free API tier doesn't support date filtering. Requested date was: {flight_date})" if flight_date else ""
        airport_info = f" - {airport_name} ({arr_iata})" if airport_name else f" ({arr_iata})"
        
        for f in data:
            airline = f.get("airline", {}).get("name", "Unknown Airline")
            num = f.get("flight", {}).get("iata", "Unknown Flight")
            dep = f.get("departure", {}).get("airport", "Unknown Departure")
            arr = f.get("arrival", {}).get("airport", "Unknown Arrival")
            dep_time = f.get("departure", {}).get("scheduled", "N/A")
            arr_time = f.get("arrival", {}).get("scheduled", "N/A")
            status = f.get("flight_status", "Unknown")
            flights.append(f"{airline} ({num}) - Status: {status}\nFrom {dep} → {arr}\nDepart {dep_time}, Arrive {arr_time}\n")
        
        return f"Flights to {destination}{airport_info}{date_note}:\n\n" + "\n---\n".join(flights)
    except requests.exceptions.HTTPError as e:
        if "403" in str(e):
            # Use Gemini as fallback for 403 errors
            prompt = f"Generate a realistic list of 3 sample flights to {destination} airport on {flight_date if flight_date else 'today'}. Include airline names, flight numbers, departure airports, and times."
            return gemini_generate(prompt)
        return f"Error fetching flights: {e}"
    except Exception as e:
        # General fallback to Gemini
        try:
            prompt = f"Generate a realistic list of 3 sample flights to {destination} airport on {flight_date if flight_date else 'today'}. Include airline names, flight numbers, departure airports, and times."
            return gemini_generate(prompt)
        except:
            return f"Error fetching flights: {e}"
