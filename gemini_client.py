# gemini_client.py
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Tuyệt đối không fallback chuỗi key thô vào code
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY is not set in environment or .env file.")

DEFAULT_MODEL = "gemini-2.5-flash"


def get_genai_client():
    return client
