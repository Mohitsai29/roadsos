import google.generativeai as genai
import streamlit as st

def get_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        import os
        return os.getenv("GEMINI_API_KEY", "")

def get_ai_guidance(situation, location_info):
    try:
        key = get_key()
        if not key:
            raise ValueError("No API key")
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""You are RoadSoS, an emergency AI assistant for road accident victims in India.
The user is at or near: {location_info}

Give specific, accurate emergency guidance for this exact situation.
Format your response clearly with:
1. IMMEDIATE STEPS (numbered, specific to the situation)
2. WHO TO CALL (specific numbers)
3. WHAT NOT TO DO (specific to this situation)
4. WHILE WAITING FOR HELP

Be specific to the situation described. Do NOT give generic advice.
Keep it clear, calm and actionable.
End with: "Help is being located. Stay calm."

Situation: {situation}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI guidance unavailable. Please call 112 immediately.\n\nError: {str(e)}"

def chat_with_ai(history, new_message, location_info):
    try:
        key = get_key()
        if not key:
            raise ValueError("No API key")
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        system = f"""You are RoadSoS, a calm and knowledgeable emergency assistant for road accidents in India.
Location context: {location_info}
Give accurate, specific, actionable advice for each question.
Never give generic responses — always address the specific question asked."""
        chat = model.start_chat(history=[
            {"role": msg["role"], "parts": [msg["content"]]}
            for msg in history
        ])
        response = chat.send_message(f"{system}\n\nUser question: {new_message}")
        return response.text
    except Exception as e:
        return f"AI unavailable. Please call 112 for emergency help.\n\nError: {str(e)}"
