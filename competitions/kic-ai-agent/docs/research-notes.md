# 리서치 노트 ([가정-확인필요] 해소용)

조사일: 2026-11-06. 모든 항목은 아래 URL에서 확인한 내용만 기재. 확인 못 한 것은 "미확인"으로 표시.

## 1. OpenDART (금융감독원)
| 항목 | 확인 내용 | 출처 |
|---|---|---|
| 이용 대상 | 개인·기업·기관 누구나 이용(인증키 발급) | https://opendart.fss.or.kr/intro/main.do |
| 제공 범위 | 공시 원문, 주요 공시·재무 정보, 상장사(유가/코스닥) 및 일부 비상장 대형사 재무 데이터 | 위와 동일 |
| 재무제표 커버리지 | 전체 재무제표 API(`fnlttSinglAcntAll`): 2015년 이후, 사업/반기/분기, 연결(CFS)·별도(OFS). `rcept_no`로 DART 뷰어 링크 생성 가능 | https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020 |
| 호출 한도 | 오류코드 020: "일반적으로 20,000건 이상의 요청" 시 발생(한도가 다르게 설정된 경우 그에 준함). 일부 API는 조회 회사 수 100건 초과 시 오류(021) | https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020031 |
| 약관 | 저작권은 금감원에 있고, 약관에 없는 사항은 저작권법·공공데이터법에 따름. 서비스 오남용 시 이용 중지 가능 | https://opendart.fss.or.kr/intro/terms.do |
| 미확인 | 분당 호출 제한, 재배포 허용 범위의 세부 문구(약관 전문 재독 필요) | - |

## 2. 뉴스 소스
| 후보 | 확인 내용 | 판단 | 출처 |
|---|---|---|---|
| 네이버 검색 API(뉴스) | 일 25,000회. 약관(2026-10-07 개정): 데이터의 복사·저장·캐싱, **AI 입력·학습·평가 활용 금지**, 임시 캐시만 허용(서버 이력 최대 21일 등) | **LLM 입력용으로 사용 불가**. 제외 | https://developers.naver.com/docs/serviceapi/search/news/news.md , https://developers.naver.com/products/terms/ , https://developers.naver.com/notice/article/33400 |
| GDELT | 제3자 정리문서 기준: 무료·개방, 키 불필요, 문서화된 하드 한도 없음, 기사 본문 저작권은 언론사 소유(메타데이터·분석만 제공). 공식 약관 원문은 미재확인 | 제목·URL·메타데이터 수준으로 사용 가능성 있음. 공식 약관 확인 후 확정 | https://github.com/DRM3Labs/drm3-data-licenses/blob/main/third-party/gdelt.md (2차 출처) |
| 언론사 RSS | 이번 조사에서 개별 약관 미확인 | 매체별 약관 확인 후 사용 | - |

결론: MVP 뉴스는 **샘플/합성 뉴스 + (선택) 제목·링크 수준 메타데이터**로 제한하고, 본문 재배포·저장은 하지 않는다.

## 3. 통계(시장 규모·업무량·자동화 효과)
- 신뢰할 만한 국내 애널리스트 리서치 업무량/시장 규모 통계는 이번 조사에서 **찾지 못함**. 수치를 만들지 않는다.
- 업계 사례(벤더 주장, 독립 검증 아님): Rogo는 OpenAI 사례 페이지에서 "분석가당 주 10시간 이상 절감"을 주장. https://openai.com/index/rogo/ — 제안서에 쓸 경우 "벤더 주장"으로 명시.
- 권고: 시장 규모는 **삭제**, 효과 수치는 "파일럿에서 측정할 지표(작성 시간, 수치 오류 건수)"로 표기하고 **추정** 라벨 유지.

## 4. 유사 서비스 비교
| 서비스 | 확인된 특징 | 출처 |
|---|---|---|
| AlphaSense (Generative Search) | 답변에 원문 문서로 연결되는 인라인 인용(문서·페이지 deep link). 재무·컨센서스 정형 데이터를 답변에 통합, 22K+ 상장사 | https://developer.alpha-sense.com/agent-api/response-parsing , https://help.alpha-sense.com/hc/en-us/articles/48564174120595-Financial-Data-Integration-into-Generative-Search |
| Hebbia (Matrix) | 표 형태 추출 결과의 각 셀에 원문 문장 연결 인용. 엔터프라이즈 데모 신청 방식 | https://www.hebbia.com/blog/5-ways-equity-research-teams-use-hebbia-to-drive-speed-and-insight , https://aicurated.io/tools/hebbia/ (2차) |
| Rogo | 은행/PE 대상 금융 특화 플랫폼, SEC 공시·S&P·FactSet 등 외부 데이터 + 내부 문서, 실사·자료 생성 | https://openai.com/index/rogo/ , https://moge.ai/product/rogo (2차) |

비교(공개 자료로 확인된 범위만; "미확인"은 해당 자료에 언급 없음):
| 기능 | AlphaSense | Hebbia | Rogo | 본 제안(PeerCheck) |
|---|---|---|---|---|
| 주장-출처 연결 | 있음(인라인 인용) | 있음(셀 단위) | 미확인 | 있음(Claim Ledger) |
| 수치 코드 재계산 검증 | 미확인 | 미확인 | 미확인 | 있음(설계) |
| 뉴스-공시 상충 플래그 | 미확인 | 미확인 | 미확인 | 있음(설계) |
| 근거 없는 문장 "확인 불가" 처리 | 미확인 | 미확인 | 미확인 | 있음(설계) |
| 한국 DART 특화 | 미확인 | 미확인 | 미확인 | 있음 |
| 접근성 | 유료/엔터프라이즈 | 데모 신청 | 엔터프라이즈 | 오픈 소스 MVP |

정직한 평가: **출처 인용 자체는 차별점이 아니다**(AlphaSense·Hebbia가 이미 제공). 차별점은 "수치 재계산·상충 탐지·확인 불가 표기를 검증 단계로 명시"와 "DART 기반 한국 공시 특화"이며, 이 부분이 경쟁사에 없다고 단정할 수 없다(비공개 기능 가능). 제안서는 "공개 자료에서 확인되지 않음"으로 서술한다. 중복 비율 등 수치는 제시하지 않는다.

## 5. 오픈소스 라이선스 (공식 저장소 LICENSE, 2026-11-06 확인)
| 라이브러리 | 라이선스 | 출처 |
|---|---|---|
| LangGraph | MIT (Copyright 2024 LangChain, Inc.) | https://raw.githubusercontent.com/langchain-ai/langgraph/main/LICENSE |
| FastAPI | MIT (Copyright 2018 Sebastián Ramírez) | https://raw.githubusercontent.com/fastapi/fastapi/master/LICENSE |
| Streamlit | Apache License 2.0 | https://raw.githubusercontent.com/streamlit/streamlit/develop/LICENSE |

## 해소 현황
- 해소: OSS 라이선스, OpenDART 범위·한도·약관 개요, 유사 서비스 비교, 네이버 뉴스 API 제외 결정.
- 부분 해소(마커 유지): 뉴스 제공처(GDELT 공식 약관 미확인), 효과 정량 수치(파일럿 측정), 업무량·오류 빈도(근거 없음).
- 삭제 권고: 시장 규모.
- 해소(2026-11-06 2차): GDELT 공식 약관(https://www.gdeltproject.org/about.html#termsofuse): 모든 데이터셋은 학술·상업·정부 용도로 무료·무제한 이용 가능, 재배포 가능하되 GDELT 출처 및 웹사이트 링크 표기 필수. → 선택 연동으로 채택.
- 해소: OpenDART 약관(https://opendart.fss.or.kr/intro/terms.do) 제10조 ④⑥: 허용량은 홈페이지 게시, 과도한 접속은 제한 가능. 분당 제한은 약관에 명시 없음. 제16조: 저작권은 금감원, 그 외는 저작권법·공공데이터법. 제23조: 공시 정확성은 금감원이 보장하지 않음. → 캐시·재시도, 원문 재배포 없이 DART 링크 연결로 서술.
- 정량 효과·업무량: 근거 통계 없음 → 파일럿 측정 가설로 서술(수작업 대비 작성 시간, 수치 불일치 건수, 출처 연결률). 시장 규모는 삭제.
- LLM: 선정 기준(수치·인용 정확도, 비용, 한국어, 교체 가능 인터페이스)을 팀 계획으로 기술, 최종 모델은 평가 후 확정.
- 미종결: OpenDART 분당 호출 제한의 공식 수치(문서에 없음) — "명시되지 않음"으로 서술.
