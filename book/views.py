import json
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from readinglists.services import reading_list_create_default

from .constants import BOOK_FIELD_NAMES, GENRE_CHOICES, TOPIC_CHOICES
from .methods import buscar_libros
from .selectors import books_recommended, disliked_book_titles
from .services import disliked_book_add, history_create

logger = logging.getLogger(__name__)


def faq(request):
    return render(request, "faq.html")


def index(request):
    return render(request, "index.html")


def recomendations(request):
    return render(request, "recomendations.html", {"books": books_recommended()})


@require_POST
def response(request):
    books = _selected_values(request.POST, BOOK_FIELD_NAMES)
    topics = _selected_values(request.POST, TOPIC_CHOICES)
    genres = _selected_values(request.POST, GENRE_CHOICES)
    details = request.POST.get("message", "").strip()
    if not books:
        return render(request, "index.html", {"error": "Selecciona al menos un libro."})
    recommendations = _recommend_books(
        request.user if request.user.is_authenticated else None,
        books,
        topics,
        genres,
        details,
        request.POST.get("longitud", ""),
    )
    if request.user.is_authenticated:
        history_create(user=request.user, books=books, topics=topics, genres=genres)
    return render(
        request, "response.html", {"respuesta": "", "libros": recommendations}
    )


def _selected_values(post_data, fields):
    return [
        post_data[field].strip() for field in fields if post_data.get(field, "").strip()
    ]


def _recommend_books(user, books, topics, genres, details, length):
    titles = _openai_recommendations(user, books, topics, genres, details, length)
    return [result for title in titles if (result := buscar_libros(title))]


def _openai_recommendations(user, books, topics, genres, details, length):
    if not settings.OPENAI_API_KEY:
        logger.warning("Recommendation requested without OPENAI_API_KEY")
        return []
    try:
        import openai

        excluded = disliked_book_titles(user=user) if user else []
        if user:
            reading_list = reading_list_create_default(user=user)
            excluded.extend(reading_list.books.values_list("title", flat=True))
        prompt = (
            "Recomienda al menos 10 libros en español. Responde solo como 'título - autor', "
            f"separados por punto y coma. Libros de referencia: {', '.join(books)}. "
            f"Temas: {', '.join(topics)}. Géneros: {', '.join(genres)}. Longitud: {length}. "
            f"Detalles: {details}. No recomiendes: {', '.join(excluded)}."
        )
        openai.api_key = settings.OPENAI_API_KEY
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=900,
        )
        return [
            item.strip()
            for item in completion.choices[0]
            .message["content"]
            .replace('"', "")
            .split(";")
            if item.strip()
        ]
    except Exception:
        logger.exception("Recommendation provider failed")
        return []


@login_required
@require_POST
def markAsNotRecommended(request):
    try:
        data = json.loads(request.body)
    except (TypeError, json.JSONDecodeError):
        return JsonResponse({"error": "Datos JSON inválidos."}, status=400)
    title, author = (
        (data.get("title") or "").strip(),
        (data.get("author") or "").strip(),
    )
    if not title or not author:
        return JsonResponse(
            {"error": "El título y el autor son obligatorios."}, status=400
        )
    disliked_book_add(user=request.user, title=title, author=author)
    return JsonResponse({"message": "No te recomendaremos más este libro."})
