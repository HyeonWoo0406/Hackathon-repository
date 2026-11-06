# 외부 자원 기록표

외부 데이터·모델·API는 사용 시 반드시 아래에 기록한다. 합법적으로 사용 가능하고 독창적인 자원만 사용한다.

| 종류 | 이름 | 출처(URL) | 수집일 | 라이선스 | 전처리 | 용도 |
|------|------|-----------|--------|----------|--------|------|
| 데이터 | 합성 샘플 기업/문서 (`app/tools.py`) | 자체 제작 | 2026-11-06 | 자체 저작물 | 없음 (가상 수치) | 데모 |
| 모델 | Mock LLM (`app/llm/mock.py`) | 자체 제작 | 2026-11-06 | 자체 저작물 | - | 오프라인 데모 |
| API/모델 | OpenAI Chat Completions (선택) | https://platform.openai.com | - | OpenAI 이용약관 | - | 선택적 LLM |
| API(예정) | OpenDART | https://opendart.fss.or.kr/intro/terms.do | 2026-11-06(약관 확인) | 금감원 약관, 저작권법·공공데이터법 준용 | 계정과목 정규화, 단위 통일 | 공시·재무 근거 |
| 뉴스(후보) | GDELT DOC API | https://www.gdeltproject.org/ | 미수집 | 공식 약관 확인 필요 | 제목·URL 메타데이터만 사용 | 뉴스-공시 대조 |
| 제외 | 네이버 검색 API(뉴스) | https://developers.naver.com/products/terms/ | 2026-11-06 | 약관상 AI 입력·저장 금지 | - | 사용 안 함 |
| 라이브러리 | LangGraph | https://github.com/langchain-ai/langgraph | 2026-11-06 | MIT | - | Agent 프레임워크 |
| 라이브러리 | FastAPI | https://github.com/fastapi/fastapi | 2026-11-06 | MIT | - | 백엔드 |
| 라이브러리 | Streamlit | https://github.com/streamlit/streamlit | 2026-11-06 | Apache-2.0 | - | UI |
