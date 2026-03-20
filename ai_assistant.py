import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_guidance(situation, location_info):
    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = f"""
    You are RoadSoS, an emergency AI assistant for road accident victims in India.
    The user is at or near: {location_info}

    Respond with:
    1. Immediate safety steps (numbered, simple, clear)
    2. Who to call first
    3. What NOT to do
    Keep it short, calm, and very clear. Use simple English.
    Always end with: "Help is being located. Stay calm."
    """

    response = model.generate_content(f"{system_prompt}\n\nSituation: {situation}")
    return response.text

def chat_with_ai(history, new_message, location_info):
    model = genai.GenerativeModel("gemini-1.5-flash")

    system = f"""You are RoadSoS, a calm emergency assistant for road accidents in India.
    Location context: {location_info}. Give short, clear, actionable advice only."""

    chat = model.start_chat(history=[
        {"role": msg["role"], "parts": [msg["content"]]}
        for msg in history
    ])

    response = chat.send_message(f"{system}\n\nUser: {new_message}")
    return response.text
