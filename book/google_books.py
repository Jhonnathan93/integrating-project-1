import logging
import time
from typing import Any, Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)
GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"
REQUEST_TIMEOUT_SECONDS = 10
MAX_RETRY_ATTEMPTS = 3
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def search_book(*, title: str, author: str) -> Optional[dict[str, Any]]:
    params = {
        "q": _search_query(title=title, author=author),
        "orderBy": "relevance",
        "printType": "books",
        "langRestrict": "es",
    }
    if settings.GOOGLE_BOOKS_API_KEY:
        params["key"] = settings.GOOGLE_BOOKS_API_KEY
    response = _request_volumes(params=params)
    if response is None:
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
            book_title = info.get("title", title)
            book_authors = info.get("authors") or [author]
            book_description = description
            book_cover = cover
            return {
                "title": book_title,
                "author": ", ".join(book_authors),
                "cover": cover,
                "description": book_description,
                "rating": info.get("averageRating", 0),
                "year_publication": _publication_year(info.get("publishedDate")),
                "topics": ", ".join(info.get("categories", [])),
                "isbn": isbn,
                "buy_link": info.get("infoLink", ""),
                # Legacy response template fields. They can be removed when the
                # template is migrated to the canonical English data contract.
                "titulo": book_title,
                "autores": book_authors,
                "imagen_enlace": book_cover,
                "descripcion": book_description,
            }
    return None


def _search_query(*, title: str, author: str) -> str:
    query = f"intitle:{title}"
    return f"{query}+inauthor:{author}" if author else query


def _request_volumes(*, params: dict[str, str]) -> Optional[requests.Response]:
    """Request Google Books data, retrying only temporary provider failures."""

    for attempt in range(MAX_RETRY_ATTEMPTS):
        try:
            response = requests.get(
                GOOGLE_BOOKS_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS
            )
        except requests.RequestException:
            logger.warning("Google Books request could not be completed.")
            return None

        if response.status_code not in RETRYABLE_STATUS_CODES:
            try:
                response.raise_for_status()
            except requests.RequestException:
                logger.warning(
                    "Google Books request failed with status %s.", response.status_code
                )
                return None
            return response

        if attempt < MAX_RETRY_ATTEMPTS - 1:
            delay_seconds = 0.5 * (2**attempt)
            logger.warning(
                "Google Books returned %s; retrying in %s seconds.",
                response.status_code,
                delay_seconds,
            )
            time.sleep(delay_seconds)

    logger.warning("Google Books remained unavailable after retries.")
    return None


def _publication_year(value: Optional[str]) -> int:
    try:
        return int((value or "").split("-", 1)[0])
    except ValueError:
        return 0
