import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_guidance(situation, location_info):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""You are RoadSoS, an emergency AI assistant for road accident victims in India.
The user is at or near: {location_info}

Respond with:
1. Immediate safety steps (numbered, simple, clear)
2. Who to call first
3. What NOT to do
Keep it short, calm, and very clear. Use simple English.
Always end with: "Help is being located. Stay calm."

Situation: {situation}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"""**Immediate Steps:**
1. Call 112 (Emergency) immediately
2. Do not move injured persons unless there is fire risk
3. Turn on hazard lights
4. Keep the person calm and conscious
5. Apply pressure to any bleeding wounds

**Call:** 112 (Police/Ambulance), 108 (Ambulance), 100 (Police)

**Do NOT:** Move unconscious victims, remove helmets, give water to unconscious persons.

Help is being located. Stay calm."""

def chat_with_ai(history, new_message, location_info):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        system = f"""You are RoadSoS, a calm emergency assistant for road accidents in India.
Location context: {location_info}. Give short, clear, actionable advice only."""
        chat = model.start_chat(history=[
            {"role": msg["role"], "parts": [msg["content"]]}
            for msg in history
        ])
        response = chat.send_message(f"{system}\n\nUser: {new_message}")
        return response.text
    except Exception as e:
        return "Please call 112 for immediate emergency help. Stay calm and keep others safe."
