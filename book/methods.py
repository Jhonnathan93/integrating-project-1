"""Backward-compatible helpers; business operations live in services.py."""

from .google_books import search_book
from .services import history_create


def save_history(request, _books, _topics, _genres):
    return history_create(
        user=request.user,
        books=_books.split(", "),
        topics=_topics.split(", "),
        genres=_genres.split(", "),
    )


def search_recommended_book(query):
    title, separator, author = query.partition(" - ")
    normalized_title = title.strip()
    normalized_author = author.strip() if separator else ""
    book = search_book(title=normalized_title, author=normalized_author)
    return [book or _fallback_book(normalized_title, normalized_author)]


def _fallback_book(title: str, author: str) -> dict[str, object]:
    """Keep the AI recommendation visible while the metadata provider is unavailable."""

    return {
        "title": title,
        "author": author or "Unknown author",
        "cover": "",
        "description": "Metadata is temporarily unavailable. Please try again later.",
        "rating": 0,
        "year_publication": 0,
        "topics": "",
        "isbn": "N/A",
        "buy_link": "",
        # Legacy response template fields. They can be removed when the template
        # is migrated to the canonical English data contract.
        "titulo": title,
        "autores": [author] if author else ["Unknown author"],
        "imagen_enlace": "",
        "descripcion": "Metadata is temporarily unavailable. Please try again later.",
    }
