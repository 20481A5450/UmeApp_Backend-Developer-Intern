import os
import json
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import QueryLog
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Predefined actions
ACTIONS = {
    "ORDER_FOOD": "Order Food Online",
    "FIND_RECIPE": "Find Pizza Recipes",
    "ASK_HELP": "Ask for Help",
    "SHARE_NEWS": "Share News"
}

# Suggest action(s) based on tone and intent
def suggest_actions(tone, intent):
    suggestions = []
    if intent == "Order Food":
        suggestions.append({"action_code": "ORDER_FOOD", "display_text": ACTIONS["ORDER_FOOD"]})
        suggestions.append({"action_code": "FIND_RECIPE", "display_text": ACTIONS["FIND_RECIPE"]})
    elif intent == "Ask Question":
        suggestions.append({"action_code": "ASK_HELP", "display_text": ACTIONS["ASK_HELP"]})
    return suggestions[:3]

# View to handle POST /api/analyze/
class AnalyzeView(APIView):
    def post(self, request):
        query = request.data.get("query", "")

        if not query:
            return Response({"error": "Query field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Prepare prompt for Gemini
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

            # Call Gemini model
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)

            if not response.text:
                raise ValueError("Empty response from Gemini")

            result = json.loads(response.text)
            tone = result.get('tone', 'Unknown')
            intent = result.get('intent', 'Unknown')

            suggestions = suggest_actions(tone, intent)

            # Save to database
            QueryLog.objects.create(
                query=query,
                tone=tone,
                intent=intent,
                suggested_actions=suggestions
            )

            return Response({
                "query": query,
                "analysis": {"tone": tone, "intent": intent},
                "suggested_actions": suggestions
            })

        except json.JSONDecodeError:
            return Response({"error": "Failed to parse Gemini response as JSON."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            pass