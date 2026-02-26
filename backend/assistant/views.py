from pathlib import Path
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from .models import Question, Answer
from .tools import web_search
from .utils import (
    build_prompt,
    build_web_prompt,
    get_cloud_ollama_response,
)


# ===============================
# Load knowledge base once at startup
# ===============================
BASE_PATH = Path(__file__).parent
KNOWLEDGE_BASE = ""

for file in os.listdir(BASE_PATH / "local_knowledge"):
    if file.endswith(".txt"):
        with open(BASE_PATH / "local_knowledge" / file, "r", encoding="utf-8") as f:
            KNOWLEDGE_BASE += f.read() + "\n"


# ===============================
# API View
# ===============================
@api_view(["POST"])
def ask_assistant(request):
    """
    Ask the assistant a question.

    Args:
        request: HTTP request

    Returns:
        HTTP response
    """

    question = request.data.get("question")

    if not question:
        return Response(
            {"detail": "Please provide a question."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    print("========================KNOWLEDGE_BASE=============================\n")
    print(KNOWLEDGE_BASE)

    # Try knowledge base
    kb_prompt = build_prompt(question, KNOWLEDGE_BASE)
    response = get_cloud_ollama_response(kb_prompt).strip()
    print("========================kb_prompt=============================\n")
    print(kb_prompt)
    print("========================response=============================\n")
    print(response)
    # If KB has no answer → use web search
    if "web_search" in response:
        try:
            results = web_search(question)
            if not results:
                return "Information non disponible."

            combined_web_context = "\n\n".join(
                page["content"] for page in results if page.get("content")
            )
            web_prompt = build_web_prompt(question, combined_web_context)
            response = get_cloud_ollama_response(web_prompt).strip()
            print("========================web_prompt=============================\n")
            print(web_prompt)
        except Exception as e:
            return Response(
                {"detail": "Web search failed.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    with transaction.atomic():
        # Save question
        question_to_save = Question.objects.create(user=request.user, question=question)
        # Save answer
        Answer.objects.create(question=question_to_save, answer=response)

    return Response({"answer": response}, status=status.HTTP_200_OK)
