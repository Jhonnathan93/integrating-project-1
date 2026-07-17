"""LLM provider abstractions for book recommendations."""

from typing import Protocol

from django.conf import settings

class RecommendationProvider(Protocol):
    """Contract implemented by any text-generation provider."""

    def generate_recommendations(self, *, prompt: str) -> list[str]:
        """Return recommended titles parsed from a provider response."""
        ...


class OpenAIRecommendationProvider:
    """OpenAI adapter kept for deployments that use the OpenAI API."""

    def generate_recommendations(self, *, prompt: str) -> list[str]:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")

        import openai

        openai.api_key = settings.OPENAI_API_KEY
        completion = openai.ChatCompletion.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=900,
        )
        return _parse_titles(completion.choices[0].message["content"])


class GroqRecommendationProvider:
    """Groq adapter using its official Python SDK."""

    def generate_recommendations(self, *, prompt: str) -> list[str]:
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")

        from groq import Groq

        client = Groq(api_key=settings.GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=900,
        )
        return _parse_titles(completion.choices[0].message.content)


def get_recommendation_provider() -> RecommendationProvider:
    """Build the configured provider without exposing it to the view layer."""

    providers: dict[str, RecommendationProvider] = {
        "groq": GroqRecommendationProvider(),
        "openai": OpenAIRecommendationProvider(),
    }
    try:
        return providers[settings.LLM_PROVIDER]
    except KeyError as error:
        supported = ", ".join(sorted(providers))
        raise ValueError(
            f"Unsupported LLM_PROVIDER '{settings.LLM_PROVIDER}'. Use: {supported}."
        ) from error


def _parse_titles(content: str | None) -> list[str]:
    """Normalize the agreed semicolon-separated title response format."""

    response_items = (content or "").replace('"', "").split(";")
    return [item.strip() for item in response_items if item.strip()]
