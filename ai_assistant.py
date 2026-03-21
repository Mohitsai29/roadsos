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
            raise ValueError("No API key found")
        genai.configure(api_key=key)

        # Try models in order until one works
        models_to_try = [
            "gemini-pro",
            "gemini-1.0-pro",
            "gemini-1.5-pro-latest",
            "gemini-1.5-flash",
        ]

        last_error = None
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                prompt = f"""You are RoadSoS, an emergency AI assistant for road accident victims in India.
The user is at or near: {location_info}

Give specific, accurate emergency guidance for this exact situation.
Format your response clearly with:
1. IMMEDIATE STEPS (numbered, specific to the situation)
2. WHO TO CALL (specific numbers for India)
3. WHAT NOT TO DO (specific to this situation)
4. WHILE WAITING FOR HELP

Be specific to the situation described. Do NOT give generic advice.
Keep it clear, calm and actionable.
End with: "Help is being located. Stay calm."

Situation: {situation}"""
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                last_error = e
                continue

        return f"AI unavailable. Please call 112 immediately.\n\nError: {str(last_error)}"

    except Exception as e:
        return f"AI guidance unavailable. Please call 112 immediately.\n\nError: {str(e)}"

def chat_with_ai(history, new_message, location_info):
    try:
        key = get_key()
        if not key:
            raise ValueError("No API key found")
        genai.configure(api_key=key)

        models_to_try = [
            "gemini-pro",
            "gemini-1.0-pro",
            "gemini-1.5-pro-latest",
            "gemini-1.5-flash",
        ]

        last_error = None
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                system = f"""You are RoadSoS, a calm and knowledgeable emergency assistant for road accidents in India.
Location context: {location_info}
Give accurate, specific, actionable advice for each question.
Never give generic responses — always address the specific question asked."""
                chat = model.start_chat(history=[
                    {"role": msg["role"], "parts": [msg["content"]]}
                    for msg in history
                ])
                response = chat.send_message(
                    f"{system}\n\nUser question: {new_message}")
                return response.text
            except Exception as e:
                last_error = e
                continue

        return f"AI unavailable. Please call 112.\n\nError: {str(last_error)}"

    except Exception as e:
        return f"AI unavailable. Please call 112.\n\nError: {str(e)}"
