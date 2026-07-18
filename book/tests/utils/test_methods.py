from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from book.methods import _fallback_book, search_recommended_book


class RecommendationMetadataTests(SimpleTestCase):
    def test_fallback_book_keeps_recommendation_visible_without_metadata(self) -> None:
        book = _fallback_book("Dune", "Frank Herbert")

        self.assertEqual(book["title"], "Dune")
        self.assertEqual(book["author"], "Frank Herbert")
        self.assertEqual(book["isbn"], "N/A")

    @patch("book.methods.search_book")
    def test_search_recommended_book_returns_provider_metadata(self, search_book: Mock) -> None:
        metadata = {"title": "Dune", "author": "Frank Herbert"}
        search_book.return_value = metadata

        result = search_recommended_book("Dune - Frank Herbert")

        self.assertEqual(result, [metadata])
        search_book.assert_called_once_with(title="Dune", author="Frank Herbert")

    @patch("book.methods.search_book", return_value=None)
    def test_search_recommended_book_uses_fallback_for_missing_metadata(
        self, search_book: Mock
    ) -> None:
        result = search_recommended_book("Dune")

        self.assertEqual(result[0]["author"], "Unknown author")
        search_book.assert_called_once_with(title="Dune", author="")
