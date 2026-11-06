# KIC AI Agent 공모전 — 투자 리서치 에이전트 (MVP)

국부펀드 KIC AI 에이전트 공모전 출품 프로젝트. 단순 Q&A 챗봇이 아니라, 사용자의 목표를 이해하고 **도구(검색·비교)를 사용해 근거가 인용된 리서치 보고서**를 만드는 AI Agent입니다.

- 공모전: https://daker.ai/public/hackathons/kic-ai-agent-competition
- 주제: 투자·금융 업무 혁신 AI Agent (문제는 자유 정의)
- 현재 문제 정의(초안): 투자 애널리스트의 기업/피어그룹 리서치 — 자료 탐색·비교·보고서 작성 자동화
- 일정: 예선 제안서 PDF(10p) 2026-11-12 10:00 / 본선 제출물 2026-12-22 10:00 / 본선 발표 2026-12-29

## 에이전트 동작 흐름

1. **계획**(`plan`): 요청을 분석해 사용할 도구 결정
2. **도구 호출**: `search_documents`(문서 검색), `compare_peers`(피어 비교표). 도구 실패는 trace에 기록하고 계속 진행
3. **보고서 작성**: LLM(Mock/OpenAI)이 근거 `[ID]`를 인용해 작성
4. **검증(환각 방어)**: 유효한 근거 ID가 없는 문장은 제거 후 경고, 검색 결과가 없으면 답변 거부

데모 데이터는 모두 **합성 샘플**(실제 기업·수치 아님)이며 화면/응답에 라벨이 표시됩니다.

## 기술 스택 (Tech used)

- Python 3.10+, FastAPI(API), Streamlit(UI), httpx
- LLM 제공자 추상화: `mock`(기본, 키 불필요) / `openai`(선택)
- 외부 데이터·모델·API는 [`docs/external-resources.md`](docs/external-resources.md)에 출처와 함께 기록

## 구조

```
app/
  main.py          FastAPI (/health, /research)
  agent.py         계획→도구호출→작성→검증 에이전트
  tools.py         도구 + 합성 샘플 데이터
  llm/             LLMProvider 인터페이스, mock, openai
ui.py              Streamlit 데모 UI
tests/             도구 사용·인용·환각 방어·API 테스트
docs/
  proposal-outline.md     예선 제안서 7개 필수 항목 개요
  evaluation-checklist.md 예선/본선 평가기준 체크리스트
  external-resources.md   외부 자원 기록표
```

## 실행 가이드 (Run guide)

```bash
cd competitions/kic-ai-agent
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env          # 기본값(mock)이면 키 불필요

pytest                          # 테스트
uvicorn app.main:app --reload   # API: http://127.0.0.1:8000/docs
streamlit run ui.py             # UI
```

API 예: `POST /research` `{"query": "알파반도체 베타전자 비교"}` → `report`, `citations`, `trace`, `flags`

OpenAI 사용: `.env`에 `LLM_PROVIDER=openai`, `OPENAI_API_KEY` 설정.

## 규칙 준수

외부 데이터·모델·API 사용 시 출처·수집일·라이선스·전처리 방법을 기록하고, 합법적으로 사용 가능한 자체 제작물만 사용합니다.
