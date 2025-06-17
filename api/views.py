from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CoupleSession


@api_view(["GET"])
def get_questions(request, mode):
    secret_word = request.GET.get("secret")
    page = int(request.GET.get("page", 1))

    # Create unique cache key
    cache_key = f"questions_{mode}_{secret_word}_{page}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response(cached_data)

    try:
        session = CoupleSession.objects.get(secret_word=secret_word)
    except CoupleSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=404)

    # Your existing question fetching logic
    # ...

    response_data = {
        "questions": questions,
        "page": page,
        "has_more": end < len(all_qs),
    }

    # Cache for 1 hour
    cache.set(cache_key, response_data, timeout=3600)

    return Response(response_data)
