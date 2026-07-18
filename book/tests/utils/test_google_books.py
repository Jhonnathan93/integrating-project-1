from unittest.mock import Mock, patch

import requests
from django.test import SimpleTestCase

from book.google_books import _publication_year, _search_query, search_book


class GoogleBooksTests(SimpleTestCase):
    def test_search_query_includes_author_only_when_present(self) -> None:
        self.assertEqual(
            _search_query(title="Dune", author="Frank Herbert"),
            "intitle:Dune+inauthor:Frank Herbert",
        )
        self.assertEqual(_search_query(title="Dune", author=""), "intitle:Dune")

    @patch("book.google_books.requests.get")
    def test_search_book_returns_normalized_book_data(self, request_get: Mock) -> None:
        response = Mock(status_code=200)
        response.json.return_value = {
            "items": [
                {
                    "volumeInfo": {
                        "title": "Dune",
                        "authors": ["Frank Herbert"],
                        "description": "A science-fiction novel.",
                        "imageLinks": {"thumbnail": "https://example.com/dune.jpg"},
                        "industryIdentifiers": [{"type": "ISBN_13", "identifier": "978"}],
                        "averageRating": 4.5,
                        "publishedDate": "1965-01-01",
                        "categories": ["Science fiction"],
                        "infoLink": "https://example.com/dune",
                    }
                }
            ]
        }
        request_get.return_value = response

        book = search_book(title="Dune", author="Frank Herbert")
        if book is None:
            self.fail("Expected a normalized Google Books response.")

        self.assertEqual(book["title"], "Dune")
        self.assertEqual(book["author"], "Frank Herbert")
        self.assertEqual(book["year_publication"], 1965)
        request_get.assert_called_once()

    @patch("book.google_books.time.sleep")
    @patch("book.google_books.requests.get")
    def test_search_book_retries_temporary_provider_failure(
        self, request_get: Mock, sleep: Mock
    ) -> None:
        unavailable_response = Mock(status_code=503)
        successful_response = Mock(status_code=200)
        successful_response.json.return_value = {"items": []}
        request_get.side_effect = [unavailable_response, successful_response]

        book = search_book(title="Dune", author="Frank Herbert")

        self.assertIsNone(book)
        self.assertEqual(request_get.call_count, 2)
        sleep.assert_called_once_with(0.5)

    @patch("book.google_books.requests.get")
    def test_search_book_returns_none_for_invalid_http_response(
        self, request_get: Mock
    ) -> None:
        response = Mock(status_code=404)
        response.raise_for_status.side_effect = requests.HTTPError("Not found")
        request_get.return_value = response

        self.assertIsNone(search_book(title="Unknown", author=""))

    def test_publication_year_returns_zero_for_invalid_values(self) -> None:
        self.assertEqual(_publication_year("2020-01-01"), 2020)
        self.assertEqual(_publication_year("unknown"), 0)
        self.assertEqual(_publication_year(None), 0)
