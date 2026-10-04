import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
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
