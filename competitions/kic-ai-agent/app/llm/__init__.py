import os

from .base import LLMProvider


def get_provider() -> LLMProvider:
    if os.getenv("LLM_PROVIDER", "mock").lower() == "openai":
        from .openai_provider import OpenAIProvider

        return OpenAIProvider()
    from .mock import MockProvider

    return MockProvider()


__all__ = ["LLMProvider", "get_provider"]
