from .base import LLMProvider


class MockProvider(LLMProvider):
    """오프라인 결정적 Mock. 프롬프트의 '[근거 ID] 내용' 줄을 인용 문장으로 변환한다."""

    def complete(self, system: str, prompt: str) -> str:
        out = []
        for line in prompt.splitlines():
            if line.startswith("[") and "]" in line:
                sid, text = line[1:].split("]", 1)
                out.append(f"- {text.strip()} [{sid}]")
        return "\n".join(out) or "- 근거를 찾지 못했습니다."
