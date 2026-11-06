from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, system: str, prompt: str) -> str:
        """프롬프트에 대한 텍스트 응답을 반환한다."""
