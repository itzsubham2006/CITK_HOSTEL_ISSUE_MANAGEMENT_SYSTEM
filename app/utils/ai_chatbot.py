import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AI_API_KEY")

SYSTEM_PROMPT = """
You are an AI assistant for CITK Hostel Management System.
Only answer hostel-related questions such as:
- hostel rules
- mess timings
- issue reporting
- complaint status
- warden and hostel info

Be polite, short, and helpful.
"""

def get_ai_reply(user_message: str) -> str:
    """
    Sends the user message to OpenAI API and returns the AI's response.
    If the API fails, returns a friendly error message.
    """
    if not API_KEY:
        return "⚠️ AI API key is not configured."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10  
        )
        print(response.status_code, response.text)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        print(f"[AI REQUEST ERROR] {e}")
        return "⚠️ AI service is temporarily unavailable."
    except KeyError:
        return "⚠️ AI service returned unexpected data."

r = requests.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {API_KEY}"})
print(r.status_code, r.text)