from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse

from book.constants import GENRE_CHOICES, TOPIC_CHOICES
from book.models import History


@tag("integration")
class RecommendationFlowIntegrationTests(TestCase):
    @patch("book.google_books.requests.get")
    @patch("book.views.get_recommendation_provider")
    def test_recommendation_flow_uses_llm_and_google_books_boundaries(
        self, provider_factory: Mock, request_get: Mock
    ) -> None:
        user = User.objects.create_user(username="reader", password="secure-password")
        self.client.force_login(user)
        provider_factory.return_value.generate_recommendations.return_value = [
            "Dune - Frank Herbert"
        ]
        metadata_response = Mock(status_code=200)
        metadata_response.json.return_value = {
            "items": [
                {
                    "volumeInfo": {
                        "title": "Dune",
                        "authors": ["Frank Herbert"],
                        "description": "A science-fiction novel.",
                        "imageLinks": {"thumbnail": "https://example.com/dune.jpg"},
                        "industryIdentifiers": [
                            {"type": "ISBN_13", "identifier": "9780441172719"}
                        ],
                        "averageRating": 4.5,
                        "publishedDate": "1965-01-01",
                        "categories": ["Science fiction"],
                        "infoLink": "https://example.com/dune",
                    }
                }
            ]
        }
        request_get.return_value = metadata_response

        response = self.client.post(
            reverse("response"),
            {
                "libro1": "Foundation",
                TOPIC_CHOICES[0]: TOPIC_CHOICES[0],
                GENRE_CHOICES[0]: GENRE_CHOICES[0],
                "message": "Space opera",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "response.html")
        self.assertContains(response, "Dune")
        self.assertTrue(History.objects.filter(user=user, books="Foundation").exists())
        provider_factory.return_value.generate_recommendations.assert_called_once()
        request_get.assert_called_once()
