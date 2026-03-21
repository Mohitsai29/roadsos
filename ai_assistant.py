import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

try:
    api_key = os.getenv("GEMINI_API_KEY") or st_secrets_get()
except:
    api_key = None

def get_key():
    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    except:
        return os.getenv("GEMINI_API_KEY")

def get_ai_guidance(situation, location_info):
    try:
        genai.configure(api_key=get_key())
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""You are RoadSoS, an emergency AI assistant for road accident victims in India.
Location: {location_info}

Respond with:
1. Immediate safety steps (numbered, simple, clear)
2. Who to call first
3. What NOT to do
Keep it short, calm, very clear. Simple English only.
Always end with: "Help is being located. Stay calm."

Situation: {situation}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return """**Immediate Steps:**
1. Call 112 immediately
2. Do not move injured persons unless fire risk
3. Turn on hazard lights
4. Keep the person calm and conscious
5. Apply pressure to any bleeding wounds

**Call:** 112 (Emergency), 108 (Ambulance), 100 (Police)

**Do NOT:** Move unconscious victims, remove helmets, give water to unconscious persons.

Help is being located. Stay calm."""

def chat_with_ai(history, new_message, location_info):
    try:
        genai.configure(api_key=get_key())
        model = genai.GenerativeModel("gemini-1.5-flash")
        system = f"""You are RoadSoS, a calm emergency assistant for road accidents in India.
Location: {location_info}. Give short, clear, actionable advice only."""
        full_history = []
        for msg in history:
            full_history.append({
                "role": msg["role"],
                "parts": [msg["content"]]
            })
        chat = model.start_chat(history=full_history)
        response = chat.send_message(f"{system}\n\nUser: {new_message}")
        return response.text
    except Exception as e:
        return "Please call 112 for immediate emergency help. Stay calm and keep others safe."
