from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase, override_settings

from book.llm_providers import (
    GroqRecommendationProvider,
    OpenAIRecommendationProvider,
    _parse_titles,
    get_recommendation_provider,
)


class RecommendationProviderTests(SimpleTestCase):
    def test_parse_titles_strips_empty_items_and_quotes(self) -> None:
        titles = _parse_titles('"Dune - Frank Herbert"; ; Foundation - Isaac Asimov')

        self.assertEqual(titles, ["Dune - Frank Herbert", "Foundation - Isaac Asimov"])

    @override_settings(LLM_PROVIDER="groq")
    def test_get_recommendation_provider_returns_configured_groq_adapter(self) -> None:
        self.assertIsInstance(get_recommendation_provider(), GroqRecommendationProvider)

    @override_settings(LLM_PROVIDER="openai")
    def test_get_recommendation_provider_returns_configured_openai_adapter(self) -> None:
        self.assertIsInstance(get_recommendation_provider(), OpenAIRecommendationProvider)

    @override_settings(LLM_PROVIDER="unsupported")
    def test_get_recommendation_provider_rejects_unknown_adapter(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported LLM_PROVIDER"):
            get_recommendation_provider()

    @override_settings(GROQ_API_KEY="test-key", GROQ_MODEL="test-model")
    @patch("groq.Groq")
    def test_groq_provider_uses_sdk_without_network_calls(self, groq_client: Mock) -> None:
        completion = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="Dune - Frank Herbert"))]
        )
        groq_client.return_value.chat.completions.create.return_value = completion

        titles = GroqRecommendationProvider().generate_recommendations(prompt="Recommend")

        self.assertEqual(titles, ["Dune - Frank Herbert"])
        groq_client.return_value.chat.completions.create.assert_called_once()

    @override_settings(OPENAI_API_KEY="test-key", OPENAI_MODEL="test-model")
    @patch("openai.OpenAI")
    def test_openai_provider_uses_sdk_without_network_calls(self, openai_client: Mock) -> None:
        openai_client.return_value.responses.create.return_value = SimpleNamespace(
            output_text="Dune - Frank Herbert; Foundation - Isaac Asimov"
        )

        titles = OpenAIRecommendationProvider().generate_recommendations(
            prompt="Recommend"
        )

        self.assertEqual(titles, ["Dune - Frank Herbert", "Foundation - Isaac Asimov"])
        openai_client.return_value.responses.create.assert_called_once()
