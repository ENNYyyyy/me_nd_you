from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CoupleSession, Question, CustomQuestion
from .models import CoupleSession

from .serializers import (
    QuestionSerializer,
    CustomQuestionSerializer,
    CoupleSessionSerializer,
)


@csrf_exempt
@api_view(["POST"])
def login_or_register(request):
    data = request.data
    partner1 = data.get("partner1_name")
    partner2 = data.get("partner2_name")
    secret = data.get("secret_word")

    if not (partner1 and partner2 and secret):
        return Response({"detail": "All fields are required."}, status=400)

    try:
        session, created = CoupleSession.objects.get_or_create(secret_word=secret)
        session.partner1_name = partner1
        session.partner2_name = partner2
        session.save()

        # Return session data
        return Response(
            {
                "success": True,
                "session": {
                    "secret": secret,
                    "partner1": partner1,
                    "partner2": partner2,
                },
                "redirect": "/modes/?secret=" + secret,
            }
        )
    except Exception as e:
        return Response({"detail": str(e)}, status=500)


from django.db.models import Q
import random


@api_view(["GET"])
def get_questions(request, mode):
    secret_word = request.GET.get("secret")

    try:
        session = CoupleSession.objects.get(secret_word=secret_word)
    except CoupleSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=404)

    if mode == "mixed":
        # get all admin questions
        admin_qs = Question.objects.all().order_by("?")  # Get 10 random admin questions
        # get all custom questions
        custom_qs = CustomQuestion.objects.filter(couple=session).order_by(
            "?"
        )  # Get 10 random custom questions
    else:
        admin_qs = Question.objects.filter(mode=mode).order_by(
            "?"
        )  # Get  random admin questions for the specific mode
        custom_qs = CustomQuestion.objects.filter(couple=session, mode=mode).order_by(
            "?"
        )  # Get  random custom questions for the specific mode

    all_questions = list(admin_qs) + list(custom_qs)
    random.shuffle(all_questions)

    # combine both types
    combined_data = []
    for q in all_questions:
        if isinstance(q, Question):
            combined_data.append({"text": q.text, "mode": q.mode, "is_custom": False})
        else:
            combined_data.append({"text": q.text, "mode": q.mode, "is_custom": True})

    return Response(combined_data)


@api_view(["POST"])
def add_custom_question(request):
    serializer = CustomQuestionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    print("Serializer errors:", serializer.errors)  # Debugging
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_custom_questions(request, secret_word, mode):
    try:
        session = CoupleSession.objects.get(secret_word=secret_word)
        # Get 10 random custom questions
        custom_qs = CustomQuestion.objects.filter(couple=session, mode=mode).order_by(
            "?"
        )
        serializer = CustomQuestionSerializer(custom_qs, many=True)
        return Response(serializer.data)
    except CoupleSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=404)


def login_page(request):
    return render(request, "game/login.html")


def mode_select_page(request):
    return render(request, "game/mode_select.html")


def play_page(request):
    return render(request, "game/play.html")
