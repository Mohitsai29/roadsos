import streamlit as st
import requests

def get_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        import os
        return os.getenv("GEMINI_API_KEY", "")

def call_gemini(prompt):
    key = get_key()
    if not key:
        raise ValueError("No API key found")

    endpoints = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={key}",
        f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={key}",
    ]

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1024}
    }

    for url in endpoints:
        try:
            r = requests.post(url, json=payload, timeout=30)
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            continue

    raise Exception("All Gemini endpoints failed. Please check your API key.")

def get_ai_guidance(situation, location_info):
    try:
        prompt = (
            "You are RoadSoS, an emergency AI assistant for road accident victims in India.\n"
            "Location: " + location_info + "\n\n"
            "Give SPECIFIC emergency guidance for this exact situation.\n"
            "Format:\n"
            "1. IMMEDIATE STEPS (numbered, specific)\n"
            "2. WHO TO CALL (India numbers)\n"
            "3. WHAT NOT TO DO\n"
            "4. WHILE WAITING FOR HELP\n\n"
            "Be specific. Not generic. Clear and calm.\n"
            "End with: Help is being located. Stay calm.\n\n"
            "Situation: " + situation
        )
        return call_gemini(prompt)
    except Exception as e:
        return (
            "AI unavailable (" + str(e)[:100] + ")\n\n"
            "Call immediately:\n"
            "112 - National Emergency\n"
            "108 - Ambulance\n"
            "100 - Police\n\n"
            "Basic steps:\n"
            "1. Move away from traffic\n"
            "2. Call 112 immediately\n"
            "3. Do not move unconscious victims\n"
            "4. Apply pressure to bleeding wounds\n"
            "5. Keep victim calm and conscious\n\n"
            "Help is being located. Stay calm."
        )

def chat_with_ai(history, new_message, location_info):
    try:
        context = ""
        for m in history[-4:]:
            context += m["role"].upper() + ": " + m["content"] + "\n"

        prompt = (
            "You are RoadSoS, an emergency assistant for road accidents in India.\n"
            "Location: " + location_info + "\n\n"
            "Previous conversation:\n" + context + "\n"
            "Give specific, accurate, actionable advice.\n\n"
            "User: " + new_message
        )
        return call_gemini(prompt)
    except Exception as e:
        return "AI unavailable (" + str(e)[:100] + "). Please call 112 for emergency help."
