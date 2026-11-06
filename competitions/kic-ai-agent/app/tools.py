"""에이전트 도구. 데이터는 모두 합성(synthetic) 샘플이며 실제 기업/수치가 아니다."""

DATA_LABEL = "합성 샘플 데이터 (실제 기업·수치 아님)"

DOCS = [
    {"id": "D1", "company": "알파반도체", "text": "알파반도체는 2025년 매출이 전년 대비 12% 성장했다고 공시했다."},
    {"id": "D2", "company": "알파반도체", "text": "알파반도체는 차세대 메모리 설비 투자로 영업이익률이 소폭 하락했다."},
    {"id": "D3", "company": "베타전자", "text": "베타전자는 2025년 매출이 전년 대비 5% 성장하고 부채비율을 낮췄다."},
    {"id": "D4", "company": "감마소재", "text": "감마소재는 원재료 가격 상승으로 이익 변동성이 확대될 수 있다고 밝혔다."},
    {"id": "D5", "company": "내부규정", "text": "투자 의사결정 보고서에는 모든 수치의 출처를 명시해야 한다(샘플 규정)."},
]

PEERS = {
    "알파반도체": {"매출성장률(%)": 12, "영업이익률(%)": 18, "부채비율(%)": 45},
    "베타전자": {"매출성장률(%)": 5, "영업이익률(%)": 11, "부채비율(%)": 30},
    "감마소재": {"매출성장률(%)": 3, "영업이익률(%)": 8, "부채비율(%)": 60},
}


def search_documents(query: str) -> list[dict]:
    """키워드가 포함된 문서(회사명 또는 본문)를 반환."""
    words = [w for w in query.split() if w]
    return [
        d for d in DOCS
        if any(w in d["company"] or w in d["text"] for w in words)
    ]


def compare_peers(companies: list[str]) -> dict:
    """회사별 지표 비교표. 출처 ID는 'T:<회사>'."""
    return {c: PEERS[c] for c in companies if c in PEERS}


TOOLS = {"search_documents": search_documents, "compare_peers": compare_peers}
