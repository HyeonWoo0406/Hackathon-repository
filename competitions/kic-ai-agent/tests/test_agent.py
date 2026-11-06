from fastapi.testclient import TestClient

from app.agent import ResearchAgent
from app.llm.base import LLMProvider
from app.llm.mock import MockProvider
from app.main import app


def test_agent_uses_tools_and_cites():
    r = ResearchAgent(MockProvider()).run("알파반도체 베타전자 비교")
    assert [t["tool"] for t in r["trace"]] == ["search_documents", "compare_peers"]
    assert r["report"] and r["citations"] and not r["flags"]


def test_refuses_without_evidence():
    r = ResearchAgent(MockProvider()).run("zzz")
    assert r["report"] == "" and r["flags"]


class Hallucinating(LLMProvider):
    def complete(self, system, prompt):
        return "- 알파반도체 매출은 100% 성장 [D1]\n- 근거 없는 주장"


def test_hallucination_guard_drops_uncited_lines():
    r = ResearchAgent(Hallucinating()).run("알파반도체")
    assert "근거 없는 주장" not in r["report"]
    assert len(r["flags"]) == 1


def test_api():
    c = TestClient(app)
    assert c.get("/health").json() == {"status": "ok"}
    assert c.post("/research", json={"query": "알파반도체"}).status_code == 200
