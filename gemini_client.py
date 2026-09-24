import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai

current_file = Path(__file__).resolve()
possible_env_paths = [
    current_file.parent / '.env',
    Path.home() / 'Documents/pythoncode/shared_config/.env',
    Path.home() / 'documents/pythoncode/shared_config/.env',
]

for env_path in possible_env_paths:
    if env_path.exists():
        load_dotenv(env_path, override=True)
        break

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAAq8yethEWgcimJFAXvcNu8_HcJ5AoAlw")
client = genai.Client(api_key=GEMINI_API_KEY)

DEFAULT_MODEL = "gemini-3.6-flash"

def generate_text(prompt: str, model_name: str = DEFAULT_MODEL) -> str:
    """Hàm sinh nội dung văn bản chuẩn"""
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text
    except Exception:
        # Fallback sang alias mới nhất nếu tên bản cụ thể chưa kích hoạt
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        return response.text

def get_genai_client():
    return client