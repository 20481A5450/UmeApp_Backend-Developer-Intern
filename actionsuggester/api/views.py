import os
import openai
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import QueryLog

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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

class AnalyzeView(APIView):
    def post(self, request):
        query = request.data.get("query", "")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"Analyze this message: '{query}' and give me its tone and intent in JSON format like {{'tone': '...', 'intent': '...'}}"}
                ]
            )
            content = response['choices'][0]['message']['content']
            result = eval(content)  # assuming response is simple {"tone": "...", "intent": "..."}
            tone, intent = result.get('tone', 'Unknown'), result.get('intent', 'Unknown')
            suggestions = suggest_actions(tone, intent)

            QueryLog.objects.create(query=query, tone=tone, intent=intent, suggested_actions=suggestions)

            return Response({
                "query": query,
                "analysis": {"tone": tone, "intent": intent},
                "suggested_actions": suggestions
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
