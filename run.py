"""
Travel Assistant Runner
Complete integration of all travel assistant components
Provides CLI, API, and programmatic interfaces
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables for LiteLLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import crew setup
try:
    from travel.crew.crew import travel_crew_setup
except ImportError:
    from crew.crew import travel_crew_setup

# =========================
# TRAVEL ASSISTANT RUNNER
# =========================

def run_travel_assistant(destination, flight_date=None, checkin_date=None, checkout_date=None):
    """
    Run the complete travel assistant with CrewAI agents.
    
    Args:
        destination: Destination city or airport code
        flight_date: Flight date in YYYY-MM-DD format (default: tomorrow)
        checkin_date: Hotel check-in date in YYYY-MM-DD format (default: tomorrow)
        checkout_date: Hotel check-out date in YYYY-MM-DD format (default: 2 days after check-in)
    
    Returns:
        Complete travel plan with flights, hotels, attractions, and advice
    """
    # Set default dates if not provided
    if not flight_date:
        flight_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not checkin_date:
        checkin_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if not checkout_date:
        checkin_dt = datetime.strptime(checkin_date, "%Y-%m-%d")
        checkout_date = (checkin_dt + timedelta(days=2)).strftime("%Y-%m-%d")
    
    print(f"\n{'='*60}")
    print(f"🌍 TRAVEL ASSISTANT - Planning Your Trip")
    print(f"{'='*60}")
    print(f"\n📍 Destination: {destination}")
    print(f"✈️  Flight Date: {flight_date}")
    print(f"🏨 Check-in: {checkin_date}")
    print(f"🏨 Check-out: {checkout_date}")
    print(f"\n{'='*60}\n")
    
    # Setup the crew
    travel_crew = travel_crew_setup()
    
    # Run the crew
    result = travel_crew.kickoff(inputs={
        "destination": destination,
        "flight_date": flight_date,
        "checkin_date": checkin_date,
        "checkout_date": checkout_date
    })
    
    print(f"\n{'='*60}")
    print("✅ FINAL TRAVEL PLAN")
    print(f"{'='*60}\n")
    print(result)
    print(f"\n{'='*60}\n")
    
    return result


def quick_search(destination):
    """
    Quick search with default dates (tomorrow for flight, tomorrow to +2 days for hotel).
    
    Args:
        destination: Destination city or airport code
    
    Returns:
        Complete travel plan
    """
    return run_travel_assistant(destination)


def custom_search(destination, flight_date, checkin_date, checkout_date):
    """
    Custom search with specific dates.
    
    Args:
        destination: Destination city or airport code
        flight_date: Flight date in YYYY-MM-DD format
        checkin_date: Hotel check-in date in YYYY-MM-DD format
        checkout_date: Hotel check-out date in YYYY-MM-DD format
    
    Returns:
        Complete travel plan
    """
    return run_travel_assistant(destination, flight_date, checkin_date, checkout_date)


# =========================
# CLI INTERFACE
# =========================

def interactive_cli():
    """Interactive command-line interface for travel planning."""
    print("\n" + "="*60)
    print("🌍 WELCOME TO TRAVEL ASSISTANT 🌍")
    print("="*60)
    print("\nPlan your perfect trip with AI-powered recommendations!")
    print("Get flights, hotels, attractions, and travel advice.\n")
    print("="*60)
    
    # Get destination
    dest = input("\n📍 Enter your travel destination (city or airport code): ").strip()
    
    if not dest:
        print("❌ Destination is required!")
        return
    
    # Ask for mode
    print("\n🎯 Choose planning mode:")
    print("1. Quick Search (use default dates)")
    print("2. Custom Search (specify dates)")
    
    mode = input("\nEnter 1 or 2 (default: 1): ").strip() or "1"
    
    if mode == "1":
        # Quick search with defaults
        print("\n✨ Using default dates (tomorrow for flight, tomorrow to +2 days for hotel)")
        run_travel_assistant(dest)
    
    else:
        # Custom search with specific dates
        print("\n📅 Enter travel dates (YYYY-MM-DD format):")
        print("   (Press Enter to use defaults)")
        
        flight_date = input("\n✈️  Flight date (default: tomorrow): ").strip() or None
        checkin_date = input("🏨 Check-in date (default: tomorrow): ").strip() or None
        checkout_date = input("🏨 Check-out date (default: 2 days after check-in): ").strip() or None
        
        run_travel_assistant(dest, flight_date, checkin_date, checkout_date)
    
    print("\n✅ Travel planning complete!")
    print("Safe travels! 🌍✈️🏨\n")


def batch_search(destinations):
    """
    Batch search for multiple destinations.
    
    Args:
        destinations: List of destination names/codes
    
    Returns:
        Dictionary of results for each destination
    """
    results = {}
    
    print(f"\n🔄 Running batch search for {len(destinations)} destinations...\n")
    
    for i, dest in enumerate(destinations, 1):
        print(f"\n[{i}/{len(destinations)}] Processing {dest}...")
        try:
            results[dest] = run_travel_assistant(dest)
        except Exception as e:
            print(f"❌ Error processing {dest}: {e}")
            results[dest] = None
    
    return results


# =========================
# API MODE
# =========================

def start_api_server(host="0.0.0.0", port=8000, reload=True, log_level="info"):
    """
    Start the FastAPI server for frontend integration.
    
    Args:
        host: Server host (default: 0.0.0.0 for external access)
        port: Server port (default: 8000)
        reload: Enable auto-reload on code changes (default: True)
        log_level: Logging level (default: info)
    """
    print(f"\n{'='*60}")
    print(f"🚀 Starting Travel Assistant API Server")
    print(f"{'='*60}")
    print(f"📡 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"� Auto-reload: {reload}")
    print(f"📝 Log level: {log_level}")
    print(f"\n🌐 Server URLs:")
    print(f"   Local:   http://localhost:{port}")
    print(f"   Network: http://{host if host != '0.0.0.0' else 'YOUR_IP'}:{port}")
    print(f"\n📚 API Documentation:")
    print(f"   Swagger UI: http://localhost:{port}/docs")
    print(f"   ReDoc:      http://localhost:{port}/redoc")
    print(f"\n🔗 API Endpoints:")
    print(f"   GET /flights/    - Search flights")
    print(f"   GET /hotels/     - Search hotels")
    print(f"   GET /tours/      - Get tour recommendations")
    print(f"   GET /advice/     - Get travel advice")
    print(f"   GET /health      - Health check")
    print(f"\n💡 Frontend Connection:")
    print(f"   Configure Next.js API routes to proxy to: http://localhost:{port}")
    print(f"   CORS is enabled for all origins")
    print(f"\n{'='*60}\n")
    
    import uvicorn
    
    try:
        from travel.api_server import app
    except ImportError:
        from api_server import app
    
    try:
        # Try to determine the correct module path
        try:
            import travel.api_server
            app_path = "travel.api_server:app"
        except ImportError:
            import api_server
            app_path = "api_server:app"
        
        uvicorn.run(
            app_path,
            host=host,
            port=port,
            reload=reload,
            log_level=log_level
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)


# =========================
# MAIN ENTRY POINT
# =========================

def main():
    """Main entry point with argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🌍 Travel Assistant - AI-powered travel planning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start API server (for frontend integration)
  python run.py --api
  
  # Start API server on custom port
  python run.py --api --port 8080
  
  # Start API server without auto-reload (production)
  python run.py --api --no-reload
  
  # Interactive CLI
  python run.py
  
  # Quick search
  python run.py --destination Dubai
  
  # Custom search with dates
  python run.py --destination Dubai --flight-date 2025-12-10 --checkin 2025-12-10 --checkout 2025-12-15
  
  # Batch search
  python run.py --batch Dubai Paris London Tokyo

Frontend Integration:
  The API server runs on http://localhost:8000 by default.
  Your Next.js app should proxy requests from /api/* to http://localhost:8000/*
  CORS is enabled for all origins.
        """
    )
    
    parser.add_argument(
        '--destination', '-d',
        type=str,
        help='Travel destination (city or airport code)'
    )
    
    parser.add_argument(
        '--flight-date', '-f',
        type=str,
        help='Flight date (YYYY-MM-DD format)'
    )
    
    parser.add_argument(
        '--checkin', '-i',
        type=str,
        help='Hotel check-in date (YYYY-MM-DD format)'
    )
    
    parser.add_argument(
        '--checkout', '-o',
        type=str,
        help='Hotel check-out date (YYYY-MM-DD format)'
    )
    
    parser.add_argument(
        '--api',
        action='store_true',
        help='Start FastAPI server for frontend integration'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='API server port (default: 8000)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='API server host (default: 0.0.0.0 for all interfaces)'
    )
    
    parser.add_argument(
        '--no-reload',
        action='store_true',
        help='Disable auto-reload (useful for production)'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        help='Logging level (default: info)'
    )
    
    parser.add_argument(
        '--batch', '-b',
        nargs='+',
        help='Batch search for multiple destinations'
    )
    
    args = parser.parse_args()
    
    # Start API server mode
    if args.api:
        start_api_server(
            host=args.host,
            port=args.port,
            reload=not args.no_reload,
            log_level=args.log_level
        )
        return
    
    # Batch search mode
    if args.batch:
        batch_search(args.batch)
        return
    
    # Single destination search
    if args.destination:
        run_travel_assistant(
            args.destination,
            args.flight_date,
            args.checkin,
            args.checkout
        )
        return
    
    # Interactive CLI mode (default)
    interactive_cli()


if __name__ == "__main__":
    main()
