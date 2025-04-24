import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def analyze_query_with_gemini(query):
    prompt = f"""
    Analyze the following message and return:
    - Tone (e.g., Happy, Angry, Sad, Urgent)
    - Intent (e.g., Order Food, Ask Question, Complain)
    
    Respond in this exact JSON format:
    {{
        "tone": "...",
        "intent": "..."
    }}
    
    Message: "{query}"
    """

    try:
        response = model.generate_content(prompt)
        if response.text:
            import json
            return json.loads(response.text)
        else:
            return {"tone": "Unknown", "intent": "Unknown"}
    except Exception as e:
        print("Gemini API error:", e)
        return {"tone": "Error", "intent": "Error"}
