import os
import logging
from dotenv import load_dotenv
from google import genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GEMINI_CLIENT")

# Automatically load environment variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize client safely (falls back to os.environ['GEMINI_API_KEY'] if not explicitly passed)
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY is not set in environment variables.")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Production standard model name
DEFAULT_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-1.5-flash"


def generate_text(prompt: str, model_name: str = DEFAULT_MODEL) -> str:
    """Generate text using Google GenAI SDK with fallback mechanism."""
    if not client:
        raise ValueError("GenAI Client is not initialized. Please verify GEMINI_API_KEY.")

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text or ""
    except Exception as exc:
        logger.warning(
            f"Failed to generate content with model '{model_name}': {exc}. "
            f"Attempting fallback to '{FALLBACK_MODEL}'..."
        )
        try:
            fallback_response = client.models.generate_content(
                model=FALLBACK_MODEL,
                contents=prompt,
            )
            return fallback_response.text or ""
        except Exception as fallback_exc:
            logger.error(f"Fallback generation also failed: {fallback_exc}")
            raise fallback_exc


def get_genai_client():
    return client
