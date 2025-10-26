"""
FastAPI Server for Travel Assistant
Provides REST API endpoints for travel planning
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables FIRST
load_dotenv()

# Set environment variables for LiteLLM (required by CrewAI)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

print(f"[DEBUG] API Keys loaded:")
print(f"  GEMINI_API_KEY: {'SET ✓' if GEMINI_API_KEY else 'NOT SET ✗'}")
print(f"  AVIATIONSTACK_KEY: {'SET ✓' if os.getenv('AVIATIONSTACK_KEY') else 'NOT SET ✗'}")
print(f"  GOOGLE_MAPS_KEY: {'SET ✓' if os.getenv('GOOGLE_MAPS_KEY') else 'NOT SET ✗'}")
print(f"  RAPIDAPI_KEY: {'SET ✓' if os.getenv('RAPIDAPI_KEY') else 'NOT SET ✗'}")

# Import routes
from routes import flight_api, hotel_api, tarvel_api, advice_api

# Create FastAPI app
app = FastAPI(
    title="Travel Assistant API",
    description="AI-powered travel planning API with flights, hotels, attractions, and advice",
    version="1.0.0"
)

# Add CORS middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(flight_api.router)
app.include_router(hotel_api.router)
app.include_router(tarvel_api.router)
app.include_router(advice_api.router)

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Travel Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "flights": "/flights/?destination=DXB&flight_date=2025-12-10",
            "hotels": "/hotels/?destination=Dubai&checkin_date=2025-12-10&checkout_date=2025-12-15",
            "tour": "/tour/?destination=Dubai",
            "advice": "/advice/?destination=Dubai"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Travel Assistant API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
