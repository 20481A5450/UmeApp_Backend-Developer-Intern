import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemma-3-27b-it")

ACTIONS = {
    "ORDER_FOOD": "Order Food Online",
    "FIND_RECIPE": "Find Pizza Recipes",
    "ASK_HELP": "Ask for Help",
    "SHARE_NEWS": "Share News"
}

def suggest_actions(tone, intent):
    suggestions = []
    if intent == "Order Food":
        suggestions.append({"action_code": "ORDER_FOOD", "display_text": ACTIONS["ORDER_FOOD"]})
        suggestions.append({"action_code": "FIND_RECIPE", "display_text": ACTIONS["FIND_RECIPE"]})
    elif intent == "Ask Question":
        suggestions.append({"action_code": "ASK_HELP", "display_text": ACTIONS["ASK_HELP"]})
    return suggestions[:3]

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
        print("Gemini raw response:", response.text)  # For debugging

        import re, json

        # Strip triple backticks and language labels if present
        cleaned = re.sub(r"```(?:json)?\s*|\s*```", "", response.text).strip()
        
        return json.loads(cleaned)

    except Exception as e:
        print("Gemini API error:", e)
        return {"tone": "Error", "intent": "Error"}
