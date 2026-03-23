import streamlit as st
import requests
import json

def get_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        import os
        return os.getenv("GEMINI_API_KEY", "")

def call_gemini(prompt):
    key = get_key()
    if not key:
        raise ValueError("No API key")

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1024
        }
    }

    response = requests.post(url, json=payload, timeout=30)

    if response.status_code == 200:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        # Try v1beta with gemini-1.5-flash
        url2 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
        response2 = requests.post(url2, json=payload, timeout=30)
        if response2.status_code == 200:
            data2 = response2.json()
            return data2["candidates"][0]["content"]["parts"][0]["text"]
        else:
            raise Exception(f"API Error {response2.status_code}: {response2.text[:200]}")

def get_ai_guidance(situation, location_info):
    try:
        prompt = f"""You are RoadSoS, an emergency AI assistant for road accident victims in India.
Location: {location_info}

Give SPECIFIC emergency guidance for this exact situation.
Format:
1. IMMEDIATE STEPS (numbered, specific)
2. WHO TO CALL (India numbers)
3. WHAT NOT TO DO
4. WHILE WAITING FOR HELP

Be specific. Not generic. Clear and calm.
End with: "Help is being located. Stay calm."

Situation: {situation}"""

        return call_gemini(prompt)

    except Exception as e:
        return f"""**Emergency Guidance** (AI unavailable - {str(e)[:100]})

**Call immediately:**
- 112 (National Emergency)
- 108 (Ambulance)
- 100 (Police)

**Basic steps:**
1. Ensure safety - move away from traffic
2. Call 112 immediately
3. Do not move unconscious victims
4. Apply pressure to bleeding wounds
5. Keep victim calm and conscious

Help is being located. Stay calm."""

def chat_with_ai(history, new_message, location_info):
    try:
        context = "\n".join([
            f"{m['role'].upper()}: {m['content']}"
            for m in history[-4:]
        ])

        prompt = f"""You are RoadSoS, an emergency assistant for road accidents in India.
Location: {location_info}

Previous conversation:
{context}

Give specific, accurate, actionable advice.

User: {new_message}"""

        return call_gemini(prompt)

    except Exception as e:
        return f"AI unavailable ({str(e)[:100]}). Please call 112 for emergency help."
```

**6.** Also update `requirements.txt` — remove `anthropic`, keep it as:
```
streamlit
requests
folium
streamlit-folium
google-generativeai
python-dotenv
geopy
