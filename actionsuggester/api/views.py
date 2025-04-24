from rest_framework.views import APIView
from rest_framework.response import Response
from .models import QueryLog
from .llm_utils import analyze_query_with_gemini, suggest_actions

class AnalyzeView(APIView):
    def post(self, request):
        query = request.data.get("query", "")

        if not query:
            return Response({"error": "Query field is required."}, status=status.HTTP_400_BAD_REQUEST)

        result = analyze_query_with_gemini(query)

        tone = result.get('tone', 'Unknown')
        intent = result.get('intent', 'Unknown')
        suggestions = suggest_actions(tone, intent)

        # Save log to database
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
