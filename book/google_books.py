import logging
from typing import Any, Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)
GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"
REQUEST_TIMEOUT_SECONDS = 10


def search_book(*, title: str, author: str) -> Optional[dict[str, Any]]:
    params = {
        "q": f"intitle:{title}+inauthor:{author}",
        "orderBy": "relevance",
        "printType": "books",
        "langRestrict": "es",
    }
    if settings.GOOGLE_BOOKS_API_KEY:
        params["key"] = settings.GOOGLE_BOOKS_API_KEY
    try:
        response = requests.get(
            GOOGLE_BOOKS_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
    except requests.RequestException:
        logger.exception("Google Books request failed")
        return None
    for item in response.json().get("items", []):
        info = item.get("volumeInfo", {})
        cover = info.get("imageLinks", {}).get("thumbnail")
        description = info.get("description")
        if cover and description:
            identifiers = info.get("industryIdentifiers", [])
            isbn = next(
                (
                    item["identifier"]
                    for item in identifiers
                    if item.get("type") in {"ISBN_13", "ISBN_10"}
                ),
                "N/A",
            )
            return {
                "title": info.get("title", title),
                "author": ", ".join(info.get("authors", [author])),
                "cover": cover,
                "description": description,
                "rating": info.get("averageRating", 0),
                "year_publication": _publication_year(info.get("publishedDate")),
                "topics": ", ".join(info.get("categories", [])),
                "isbn": isbn,
                "buy_link": info.get("infoLink", ""),
            }
    return None


def _publication_year(value: Optional[str]) -> int:
    try:
        return int((value or "").split("-", 1)[0])
    except ValueError:
        return 0
