# Travel Assistant - Complete Structure

A modular AI-powered travel planning system using CrewAI with specialized agents and FastAPI REST API.

## 📁 Project Structure

```
travel/
├── agents/                 # AI agents for different travel aspects
│   ├── __init__.py
│   ├── flight_agent.py    # Flight search specialist
│   ├── hotel_agent.py     # Hotel recommendation specialist
│   ├── tour_agent.py      # Tourist attraction specialist
│   └── advice_agent.py    # Travel advice specialist
│
├── tasks/                  # Tasks assigned to agents
│   ├── __init__.py
│   ├── flight_task.py     # Find flights
│   ├── hotel_task.py      # Find hotels
│   ├── tour_task.py       # Find attractions
│   └── advice_task.py     # Generate advice
│
├── tools/                  # API integration tools
│   ├── __init__.py
│   ├── check_flights.py   # AviationStack API
│   ├── check_hotels.py    # Booking.com API
│   ├── google_place.py    # Google Places API
│   ├── advice.py          # Gemini AI for advice
│   └── gemini.py          # Gemini helper functions
│
├── routes/                 # FastAPI routes (REST API endpoints)
│   ├── __init__.py
│   ├── flight_api.py      # GET /flights/
│   ├── hotel_api.py       # GET /hotels/
│   ├── tarvel_api.py      # GET /tour/
│   └── advice_api.py      # GET /advice/
│
├── main.py                # CLI application entry point
└── api_server.py          # FastAPI server entry point
```

## 🚀 Usage

### 1. CLI Application (CrewAI with Agents)

Run the interactive command-line interface:

```bash
cd travel
python main.py
```

Or use as a module:

```python
from travel.main import run_travel_assistant

result = run_travel_assistant(
    destination="Dubai",
    flight_date="2025-12-10",
    checkin_date="2025-12-10",
    checkout_date="2025-12-15"
)
```

### 2. REST API Server (FastAPI)

Start the API server:

```bash
cd travel
python api_server.py
```

Or using uvicorn directly:

```bash
uvicorn travel.api_server:app --reload --host 0.0.0.0 --port 8000
```

#### API Endpoints:

- **Flights**: `GET http://localhost:8000/flights/?destination=DXB&flight_date=2025-12-10`
- **Hotels**: `GET http://localhost:8000/hotels/?destination=Dubai&checkin_date=2025-12-10&checkout_date=2025-12-15`
- **Attractions**: `GET http://localhost:8000/tour/?destination=Dubai`
- **Advice**: `GET http://localhost:8000/advice/?destination=Dubai`

#### Interactive Docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. Import Individual Components

```python
# Import agents
from travel.agents import flight_agent, hotel_agent, tour_agent, advice_agent

# Import tasks
from travel.tasks import task_flights, task_hotels, task_tour, task_advice

# Import tools directly
from travel.tools.check_flights import check_flights
from travel.tools.check_hotels import check_hotels
from travel.tools.google_place import prepare_tour
from travel.tools.advice import give_advice
```

## 🔧 Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_MAPS_KEY=your_google_maps_key
AVIATIONSTACK_KEY=your_aviationstack_key
RAPIDAPI_KEY=your_rapidapi_key
```

## 📦 Dependencies

```bash
pip install crewai google-generativeai googlemaps requests python-dotenv fastapi uvicorn
```

## 🎯 Features

- **Flight Search**: Real-time flight data with AI fallback (AviationStack)
- **Hotel Search**: Hotel recommendations with ratings and prices (Booking.com)
- **Tourist Attractions**: Top-rated places to visit (Google Places)
- **Travel Advice**: Safety tips and cultural information (Gemini AI)
- **REST API**: FastAPI endpoints for all features
- **CLI Interface**: Interactive command-line tool
- **Modular Design**: Use components independently or together

## 🤖 Agents (CrewAI)

Each agent is specialized with its own role, goal, and tools:

1. **Flight Agent**: Finds the best flight options
2. **Hotel Agent**: Recommends accommodations
3. **Tour Agent**: Plans sightseeing itineraries
4. **Advice Agent**: Provides travel tips

## 🔗 API Routes (FastAPI)

All routes are RESTful and return JSON responses:

- `/flights/` - Flight search
- `/hotels/` - Hotel search
- `/tour/` - Tourist attractions
- `/advice/` - Travel advice

## 📝 Examples

### CLI Example:

```bash
python main.py
# Enter: Dubai
# Flight date: 2025-12-10
# Check-in: 2025-12-10
# Check-out: 2025-12-15
```

### API Example (curl):

```bash
# Get flights
curl "http://localhost:8000/flights/?destination=DXB&flight_date=2025-12-10"

# Get hotels
curl "http://localhost:8000/hotels/?destination=Dubai&checkin_date=2025-12-10&checkout_date=2025-12-15"

# Get attractions
curl "http://localhost:8000/tour/?destination=Dubai"

# Get advice
curl "http://localhost:8000/advice/?destination=Dubai"
```

### Python Example:

```python
import requests

# Use the API
response = requests.get("http://localhost:8000/flights/", params={
    "destination": "DXB",
    "flight_date": "2025-12-10"
})
print(response.json())
```

## 🎨 Architecture

- **Agents**: Autonomous AI agents with specific expertise
- **Tasks**: Defined objectives for agents to complete
- **Tools**: API integrations and utility functions
- **Routes**: REST API endpoints for external access
- **Main**: CLI orchestration with CrewAI
- **API Server**: FastAPI server for web access

## 📊 Use Cases

1. **Travel Planning**: Complete trip planning with one command
2. **API Integration**: Integrate travel features into your app
3. **Custom Workflows**: Build custom travel workflows with modular components
4. **Microservices**: Use as a travel planning microservice
