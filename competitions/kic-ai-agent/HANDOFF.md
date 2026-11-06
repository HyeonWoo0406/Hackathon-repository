# KIC AI 에이전트 공모전 — 인수인계 (HANDOFF)

대화 이력 없이 이어받을 수 있도록 정리한 문서입니다. API 키·비공개 정보는 포함하지 않습니다.

## 1. 대회 개요·일정
- 국부펀드 KIC, AI 에이전트 공모전: 투자·금융 업무 혁신 AI Agent 기획 + MVP 구현. 해커톤 페이지: https://daker.ai/public/hackathons/kic-ai-agent-competition
- 예선: 기획서 PDF(최대 10쪽, 필수 7개 섹션) — **2026-11-12 10:00 마감**. 동료 투표 11/12 12:00~11/19 10:00(30%), 내부 전문가 평가 ~12/01 23:59(70%).
- 본선(상위 12팀): 데모 URL·발표자료 PDF(10분)·GitHub 저장소(코드·실행 가이드)·(선택) 데모 영상 — **2026-12-22 10:00 제출**, 온라인 발표 12/29.
- 규칙: 외부 데이터·모델·API 허용, 모든 외부 자원의 출처·라이선스·수집일·전처리 기재, 합법적이고 독창적일 것. 평가 기준은 `docs/evaluation-checklist.md`.

## 2. 아이디어·팀
- **PeerCheck**: 공시·재무 근거를 자동 검증하는 Peer Group 투자리서치 LangGraph Agent. Planner → Collector(OpenDART, 뉴스 메타데이터) → Analyst → Verifier → Reporter. Claim Ledger, 코드 재계산, 뉴스-공시 충돌은 검토 큐, 근거 없으면 "확인 불가".
- 팀 표지: 팀명 **HeadLine**, 팀장 윤현우, 팀원 라로스, 밥이다.
- AI 활용 내역(10쪽): GitHub Copilot (Claude Sonnet 5.5, GPT-6 Astra).

## 3. 현재 상태
- 예선 기획서 10쪽 완성(공식 템플릿 구조 유지, 마커 없음). 제출 전 팀이 최종 검토 후 PDF 제출 필요.
- 최종 파일: `docs/submission/KIC_기획서_초안.pptx`, `.pdf` (공식 템플릿 원본 pptx는 저장소에 없음).
- 재생성: `docs/submission/build/`의 `build_pptx.py`(1·2·10쪽)와 `build_pptx_v2.py`(3~9쪽)를 사용. 공식 템플릿 pptx를 `~\.copilot\attachments\`에 두고, `OUT_DIR` 경로를 본인 환경으로 수정한 뒤 `python -X utf8 build_pptx_v2.py` 실행. 템플릿을 새로 받아야 한다면 KIC 공모전 페이지의 양식을 사용. PDF는 PowerPoint에서 PDF로 저장. 내용 원문은 `docs/proposal-draft.md`.
- 코드: `competitions/kic-ai-agent/` 스캐폴드(FastAPI + Streamlit, mock/OpenAI LLMProvider, 합성 데이터 기반 도구 사용 에이전트, 출처 표기·환각 가드). 아직 PeerCheck의 실제 LangGraph/OpenDART 연동은 미구현.

## 4. DART 확인 요약 (상세: `docs/dart-check.md`, 2026-11-06 확인)
| 기업 | 2025 사업보고서 접수번호 | 영업이익률(연결) | 부채비율 |
|---|---|---|---|
| 삼성전자 | 20260310002820 | 13.07% | 29.94% |
| SK하이닉스 | 20260317000635 | 48.59% | 45.95% |
| DB하이텍 | 20260601001661 ([기재정정], 원본 20260316001250) | 19.85% | 33.36% |

- 3사 모두 연결(CFS)·별도(OFS) 제공. 연결 우선.
- **정정본 정책**: 최신 정정본 기준, 원본 접수번호는 이력 보관, 출처에 [기재정정] 표기.
- **account_id 정규화**: 계정명이 회사마다 다르고(매출액 vs 수익(매출액)) 손익 구분도 IS/CIS로 달라 `ifrs-full_Revenue`, `dart_OperatingIncomeLoss`, `ifrs-full_Liabilities`, `ifrs-full_Equity` 기준으로 조회.
- **기간 규칙**: 분기·반기 보고서는 `thstrm_amount`(3개월)와 `thstrm_add_amount`(누적)가 함께 온다. 분자·분모는 같은 기간 필드로 계산, 기간을 Ledger에 기록, 연간/분기 혼용은 기간 불일치로 플래그.
- 기획서 8쪽의 ③은 실조회 값, ④ 충돌 기사·⑤ 확인 불가 문장은 "가상 예시".

## 5. 열린 문제
- DART 뷰어 링크 형식 `https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}` 미검증(구현 시 열어 확인).
- 3분기보고서(reprt_code 11014)는 11월 중순 제출 후 재확인.
- KPI 목표치(출처 연결률 95%, 재계산 일치율 95%, 충돌 탐지 90%, 시간 단축 50%)는 팀이 정한 목표이며, 평가셋·비교 절차는 MVP에서 측정.
- 뉴스는 샘플 기본, GDELT는 선택(공식 약관 확인 전 필수 아님). 상세는 `docs/research-notes.md`.

## 6. 본선 MVP 다음 단계 (~12/22)
1. 11월 중~하순: OpenDART Collector(account_id 정규화, 연결/별도, 정정본 정책) + 재계산 Tool.
2. 12월 초: LangGraph 5역할 그래프 + Claim Ledger(주장 유형, 허용오차, 상태 전이).
3. 12월 중순: Streamlit 검증 UI, 뉴스-공시 충돌 탐지·검토 큐.
4. ~12/22: 안정화, 데모 URL 배포, 발표자료 PDF, 실행 가이드(README), `docs/external-resources.md` 갱신, (선택) 데모 영상.

## 7. 실행 방법
```powershell
cd competitions\kic-ai-agent
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env        # .env에 DART_API_KEY=발급키 입력 (절대 커밋 금지; .env는 gitignore)
uvicorn app.main:app --reload
streamlit run ui.py
```
- Windows에서 `python`이 Microsoft Store 스텁일 수 있음 → `%LOCALAPPDATA%\Programs\Python\Python312\python.exe` 사용.
- OpenDART 키는 https://opendart.fss.or.kr 에서 발급. 코드에서는 환경변수로만 읽고 출력·로그 금지.

## 8. 새 Copilot 세션 시작 프롬프트 예시
```
저장소 HyeonWoo0406/Hackathon-repository의 브랜치 hyeonwoo0406-kic-ai-agent-setup에서 작업한다.
competitions/kic-ai-agent/HANDOFF.md와 docs/ 문서를 먼저 읽고 현재 상태를 요약해줘.
그다음 본선 MVP 1단계(OpenDART Collector + account_id 정규화 + 재계산 Tool)를 구현해줘.
DART_API_KEY는 .env에서 환경변수로만 읽고 절대 출력·커밋하지 마. PR은 열지 마.
```
