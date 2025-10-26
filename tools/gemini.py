import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment and configure Gemini
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def gemini_generate(prompt: str) -> str:
    """Generate a response using free Gemini 2.0 Flash model."""
    try:
        # use the free-tier Gemini model available in AI Studio
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        result = model.generate_content(prompt)
        return result.text.strip()
    except Exception as e:
        return f"[Gemini Error] {e}"
