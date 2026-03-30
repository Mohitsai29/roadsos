import streamlit as st
import requests

def get_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        import os
        return os.getenv("GEMINI_API_KEY", "")

def list_models():
    key = get_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        models = r.json().get("models", [])
        return [m["name"] for m in models if "generateContent" in m.get("supportedGenerationMethods", [])]
    return []

def call_gemini(prompt):
    key = get_key()
    if not key:
        raise ValueError("No API key found")

    models = list_models()
    if not models:
        raise ValueError("No models available for this API key")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1024}
    }

    for model in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={key}"
            r = requests.post(url, json=payload, timeout=30)
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            continue

    raise Exception("Available models: " + str(models[:3]))

def get_ai_guidance(situation, location_info):
    try:
        prompt = (
            "You are RoadSoS, an emergency AI assistant for road accident victims in India.\n"
            "Location: " + location_info + "\n\n"
            "Give SPECIFIC emergency guidance for this exact situation.\n"
            "Format your response with these sections:\n"
            "1. IMMEDIATE STEPS (numbered, specific to situation)\n"
            "2. WHO TO CALL (India emergency numbers)\n"
            "3. WHAT NOT TO DO (specific to situation)\n"
            "4. WHILE WAITING FOR HELP\n\n"
            "Be specific. Not generic. Clear and calm.\n"
            "End with: Help is being located. Stay calm.\n\n"
            "Situation: " + situation
        )
        return call_gemini(prompt)
    except Exception as e:
        return (
            "AI unavailable: " + str(e) + "\n\n"
            "Please call:\n"
            "112 - National Emergency\n"
            "108 - Ambulance\n"
            "100 - Police"
        )

def chat_with_ai(history, new_message, location_info):
    try:
        context = ""
        for m in history[-4:]:
            context += m["role"].upper() + ": " + m["content"] + "\n"
        prompt = (
            "You are RoadSoS, emergency assistant for road accidents in India.\n"
            "Location: " + location_info + "\n\n"
            "Conversation so far:\n" + context + "\n"
            "User: " + new_message + "\n\n"
            "Give specific, actionable emergency advice."
        )
        return call_gemini(prompt)
    except Exception as e:
        return "AI unavailable: " + str(e) + ". Call 112 for emergency help."
