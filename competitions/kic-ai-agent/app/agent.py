import re

from .llm import LLMProvider, get_provider
from .tools import DATA_LABEL, DOCS, PEERS, TOOLS

SYSTEM = (
    "당신은 투자 애널리스트용 리서치 에이전트입니다. 제공된 근거만 사용하고, "
    "모든 문장 끝에 [근거ID]를 붙이세요. 근거가 없으면 답하지 마세요."
)


class ResearchAgent:
    """계획 → 도구 호출 → 보고서 작성 → 근거 검증(환각 방어) 순으로 동작."""

    def __init__(self, llm: LLMProvider | None = None) -> None:
        self.llm = llm or get_provider()

    def plan(self, query: str) -> list[dict]:
        companies = [c for c in PEERS if c in query]
        steps = [{"tool": "search_documents", "args": {"query": query}}]
        if len(companies) >= 2 or "비교" in query:
            steps.append({"tool": "compare_peers", "args": {"companies": companies or list(PEERS)}})
        return steps

    def run(self, query: str) -> dict:
        trace, evidence = [], {}
        for step in self.plan(query):
            try:
                result = TOOLS[step["tool"]](**step["args"])
            except Exception as e:  # 도구 실패는 기록하고 계속 진행
                trace.append({**step, "error": str(e)})
                continue
            trace.append({**step, "result_count": len(result)})
            if step["tool"] == "search_documents":
                for d in result:
                    evidence[d["id"]] = d["text"]
            else:
                for c, m in result.items():
                    evidence[f"T:{c}"] = f"{c} 지표: " + ", ".join(f"{k} {v}" for k, v in m.items())

        if not evidence:
            return {"query": query, "trace": trace, "report": "", "citations": {},
                    "flags": ["검색된 근거가 없어 답변을 거부했습니다."], "data_label": DATA_LABEL}

        ctx = "\n".join(f"[{i}] {t}" for i, t in evidence.items())
        draft = self.llm.complete(SYSTEM, f"질문: {query}\n근거:\n{ctx}")
        report, flags = self.verify(draft, evidence)
        used = {i for i in re.findall(r"\[([^\]]+)\]", report) if i in evidence}
        return {"query": query, "trace": trace, "report": report,
                "citations": {i: evidence[i] for i in sorted(used)},
                "flags": flags, "data_label": DATA_LABEL}

    @staticmethod
    def verify(draft: str, evidence: dict) -> tuple[str, list[str]]:
        """유효한 근거 ID가 없는 문장은 제거하고 플래그로 남긴다."""
        kept, flags = [], []
        for line in filter(None, (l.strip() for l in draft.splitlines())):
            ids = re.findall(r"\[([^\]]+)\]", line)
            if ids and all(i in evidence for i in ids):
                kept.append(line)
            else:
                flags.append(f"근거 없는 문장 제외: {line}")
        return "\n".join(kept), flags


__all__ = ["ResearchAgent", "DOCS"]
