import google.generativeai as genai
import streamlit as st

def get_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        import os
        return os.getenv("GEMINI_API_KEY", "")

def list_available_models():
    try:
        key = get_key()
        genai.configure(api_key=key)
        models = genai.list_models()
        return [m.name for m in models if "generateContent" in m.supported_generation_methods]
    except:
        return []

def get_best_model():
    models = list_available_models()
    # Priority order
    preferred = [
        "models/gemini-1.5-pro",
        "models/gemini-1.5-flash",
        "models/gemini-1.0-pro",
        "models/gemini-pro",
        "models/gemini-2.0-flash",
        "models/gemini-2.0-flash-lite",
    ]
    for p in preferred:
        if p in models:
            return p.replace("models/", "")
    # Return first available
    if models:
        return models[0].replace("models/", "")
    return None

def get_ai_guidance(situation, location_info):
    try:
        key = get_key()
        if not key:
            raise ValueError("No API key found")
        genai.configure(api_key=key)

        model_name = get_best_model()
        if not model_name:
            raise ValueError("No compatible model found")

        model = genai.GenerativeModel(model_name)
        prompt = f"""You are RoadSoS, an emergency AI assistant for road accident victims in India.
The user is at or near: {location_info}

Give specific, accurate emergency guidance for this exact situation.
Format your response clearly with:
1. IMMEDIATE STEPS (numbered, specific to the situation)
2. WHO TO CALL (specific numbers for India)
3. WHAT NOT TO DO (specific to this situation)
4. WHILE WAITING FOR HELP

Be specific. Do NOT give generic advice.
Keep it clear, calm and actionable.
End with: "Help is being located. Stay calm."

Situation: {situation}"""
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI unavailable (Error: {str(e)})\n\nPlease call 112 immediately for emergency help."

def chat_with_ai(history, new_message, location_info):
    try:
        key = get_key()
        if not key:
            raise ValueError("No API key found")
        genai.configure(api_key=key)

        model_name = get_best_model()
        if not model_name:
            raise ValueError("No compatible model found")

        model = genai.GenerativeModel(model_name)
        system = f"""You are RoadSoS, a calm emergency assistant for road accidents in India.
Location: {location_info}. Give specific, actionable advice only."""

        chat = model.start_chat(history=[
            {"role": msg["role"], "parts": [msg["content"]]}
            for msg in history
        ])
        response = chat.send_message(f"{system}\n\nUser: {new_message}")
        return response.text

    except Exception as e:
        return f"AI unavailable (Error: {str(e)})\n\nPlease call 112 for emergency help."
