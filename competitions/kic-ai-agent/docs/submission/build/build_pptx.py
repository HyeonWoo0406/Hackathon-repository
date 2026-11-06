import copy
import glob
import os
import re

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

SRC = glob.glob(os.path.expanduser(r"~\.copilot\attachments\*.pptx"))[0]
OUT_DIR = r"C:\Users\smhrd\.copilot\session-state\9f9065b2-5430-404d-aca5-dfb6c46338cd\files"
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "KIC_기획서_초안.pptx")

NAVY = RGBColor(0x1F, 0x38, 0x64)
RED = RGBColor(0xC0, 0x00, 0x00)
GRAY = RGBColor(0x40, 0x40, 0x40)
LIGHT = RGBColor(0xE9, 0xEE, 0xF7)
MARK = "[가정-확인필요]"

prs = Presentation(SRC)
slides = list(prs.slides)

# 본문 영역 (헤딩 구분선 아래 ~ 하단 선 위)
X0, X1 = 968477, 968477 + 10255045
Y0, Y1 = 1640000, 5840000
W = X1 - X0


def add_runs(par, text, size, bold=False, color=GRAY):
    for part in re.split(r"(\[가정-확인필요[^\]]*\]|\[제출 전[^\]]*\])", text):
        if not part:
            continue
        r = par.add_run()
        r.text = part
        r.font.size = Pt(size)
        flagged = part.startswith("[가정") or part.startswith("[제출 전")
        r.font.bold = True if flagged else bold
        r.font.color.rgb = RED if flagged else color


def set_bullet(par, level_indent=171450):
    pPr = par._p.get_or_add_pPr()
    pPr.set("marL", str(level_indent))
    pPr.set("indent", str(-level_indent))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for e in pPr.findall(qn(tag)):
            pPr.remove(e)
    bu = etree.SubElement(pPr, qn("a:buChar"))
    bu.set("char", "•")


def add_text(slide, x, y, w, h, items, size=11):
    """items: ('h', text) 헤딩 / ('b', text) 불릿 / ('p', text) 일반"""
    tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(36000)
    tf.margin_top = tf.margin_bottom = Emu(18000)
    first = True
    for kind, text in items:
        par = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        par.space_after = Pt(2)
        if kind == "h":
            par.space_before = Pt(4)
            add_runs(par, text, size + 1, bold=True, color=NAVY)
        else:
            if kind == "b":
                set_bullet(par)
            add_runs(par, text, size)
    return tb


def add_table(slide, x, y, w, rows, col_w, size=10, row_h=300000, header=True):
    nrows, ncols = len(rows), len(rows[0])
    gs = slide.shapes.add_table(nrows, ncols, Emu(x), Emu(y), Emu(w), Emu(row_h * nrows))
    tbl = gs.table
    # 기본 스타일 줄무늬 제거
    tblPr = tbl._tbl.tblPr
    tblPr.set("bandRow", "0")
    tblPr.set("firstRow", "0")
    total = sum(col_w)
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Emu(int(w * cw / total))
    for r in range(nrows):
        tbl.rows[r].height = Emu(row_h)
        for c in range(ncols):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Emu(54000)
            cell.margin_top = cell.margin_bottom = Emu(22000)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            par = tf.paragraphs[0]
            is_head = header and r == 0
            add_runs(par, rows[r][c], size, bold=is_head or c == 0,
                     color=RGBColor(255, 255, 255) if is_head else GRAY)
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if is_head else (LIGHT if c == 0 else RGBColor(255, 255, 255))
    return gs


def add_flow(slide, x, y, w, h, labels, size=10):
    n = len(labels)
    gap = 220000
    bw = int((w - gap * (n - 1)) / n)
    for i, lab in enumerate(labels):
        shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(x + i * (bw + gap)), Emu(y), Emu(bw), Emu(h))
        shp.fill.solid()
        shp.fill.fore_color.rgb = NAVY
        shp.line.fill.background()
        tf = shp.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Emu(30000)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        par = tf.paragraphs[0]
        par.alignment = PP_ALIGN.CENTER
        add_runs(par, lab, size, bold=True, color=RGBColor(255, 255, 255))
        if i < n - 1:
            ar = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Emu(x + i * (bw + gap) + bw + 30000),
                                        Emu(y + h // 2 - 70000), Emu(gap - 60000), Emu(140000))
            ar.fill.solid()
            ar.fill.fore_color.rgb = RGBColor(0x7F, 0x7F, 0x7F)
            ar.line.fill.background()


def remove_guide(slide):
    for sh in list(slide.shapes):
        if sh.has_text_frame and sh.text_frame.text.startswith("[작성방법]"):
            sh._element.getparent().remove(sh._element)


def fill_cell(cell, text, size=11):
    tf = cell.text_frame
    par = tf.paragraphs[0]
    # 템플릿 서식(첫 run)을 유지하면서 텍스트만 교체
    runs = par.runs
    if runs:
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
        runs[0].text = ""
        base = runs[0]
        base._r.getparent().remove(base._r)
    for extra in tf.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    add_runs(par, text, size)


# ---------- 1. 표지 ----------
tbl = next(s for s in slides[0].shapes if s.has_table).table
fill_cell(tbl.cell(0, 1), "HeadLine", 12)
fill_cell(tbl.cell(1, 1), "윤현우", 12)
fill_cell(tbl.cell(2, 1), "라로스, 밥이다", 12)
sub = next(s for s in slides[0].shapes if s.name == "TextBox 4")
p = sub.text_frame.add_paragraph()
p.alignment = PP_ALIGN.CENTER
add_runs(p, "공시·재무 근거를 자동 검증하는 Peer Group 투자리서치 LangGraph Agent", 14, bold=True, color=NAVY)
sub.left = Emu(1500000)
sub.width = Emu(9192000)

# ---------- 2. Summary ----------
tbl = next(s for s in slides[1].shapes if s.has_table).table
rows = [
    "PeerCheck (가칭) — 공시·재무 근거를 자동 검증하는 Peer Group 투자리서치 Agent",
    "투자 애널리스트가 비교 대상 기업(2~5개)의 공시·재무·뉴스를 수작업으로 수집·비교하고 수치·주장의 출처를 확인하는 데 많은 시간이 든다. 일반 LLM 요약은 근거 없는 문장(환각)이 섞일 수 있다. 주요 사용자: 투자 리서치 담당자.",
    "Planner → Collector → Analyst → Verifier → Reporter. 모든 주장을 출처에 연결(Claim Ledger), DART 계정명 정규화·연결/별도·단위/기간 점검 후 재무 수치를 코드로 재계산, 뉴스-공시 충돌은 검토 큐로 전달, 근거 없는 문장은 '확인 불가' 처리.",
    "OpenDART 공시·재무 API, 샘플 뉴스(선택 연동 GDELT), LangGraph, 교체 가능한 LLM(선정 기준 정의), 근거 단위 검색(RAG)과 Claim Ledger(Memory), 코드 기반 재계산 Tool.",
    "근거 추적 가능한 비교 보고서로 리서치 초안 작성 시간 단축·수치 오류 감소. MVP 파일럿에서 수작업 대비 작성 시간·수치 불일치 건수·출처 연결률을 측정. 해외 공시·내부 문서 검색 등으로 확장.",
]
for i, t in enumerate(rows):
    fill_cell(tbl.cell(i, 1), t, 10.5)

# ---------- 3. 문제 정의 ----------
s = slides[2]
remove_guide(s)
add_text(s, X0, Y0, W, Y1 - Y0, [
    ("h", "대상 업무"),
    ("p", "2~5개 비교 기업(Peer Group)의 사업·재무·리스크를 비교하는 투자 리서치"),
    ("h", "현행 방식의 문제점"),
    ("b", "공시·재무제표·뉴스가 흩어져 있어 수집·정리에 시간이 많이 소요됨"),
    ("b", "수치 전사·계산 과정의 오류 가능성, 출처가 불명확한 문장이 보고서에 섞임"),
    ("b", "뉴스 보도와 공시 내용이 다를 때 이를 체계적으로 확인하기 어려움"),
    ("b", "일반 LLM 요약은 그럴듯하지만 근거 없는 문장(환각)을 생성할 수 있음"),
    ("h", "주요 사용자·업무 상황·활용 시나리오"),
    ("p", "투자 리서치 담당자가 \"A·B·C사의 최근 수익성·재무 안정성 비교\"를 요청 → 근거가 연결된 비교 보고서와 검증 요약을 수신"),
    ("h", "해결 필요성"),
    ("p", "투자 판단 자료는 신뢰성이 핵심이므로 '빠른 요약'보다 '검증 가능한 요약'이 필요함"),
    ("h", "확인 필요"),
    ("p", "검증 가설: 수작업 비교 리서치는 시간이 많이 들고 수치 전사 오류가 생길 수 있다. 파일럿에서 동일 과제(기업 3개)를 수작업과 Agent로 수행해 작성 시간·수치 불일치 건수를 비교. 시장 규모는 공개 근거가 없어 다루지 않음. 유사 서비스(AlphaSense·Hebbia 등)는 출처 인용을 이미 제공 — 중복 인정"),
], 13)

# ---------- 4. 서비스 제안 및 차별성 ----------
s = slides[3]
remove_guide(s)
add_text(s, X0, Y0, W, 520000, [
    ("h", "서비스 개요"),
    ("p", "비교 요청을 받아 공시·재무 데이터를 수집·분석하고, 모든 주장을 검증한 뒤 근거가 연결된 보고서를 생성하는 Agent"),
], 11)
add_flow(s, X0, Y0 + 600000, W, 520000, [
    "사용자 입력\n기업 2~5개 + 관점", "Agent 수행\n계획·수집·분석·검증",
    "최종 결과물\n비교 보고서 + 검증 요약"], 10.5)
add_text(s, X0, Y0 + 1200000, W, 300000, [("h", "차별점")], 11)
add_table(s, X0, Y0 + 1500000, W, [
    ["차별점", "설명"],
    ["Claim Ledger", "보고서의 모든 주장을 출처(공시 접수번호·계정과목, 기사 URL 등)에 연결하고 주장별 출처를 하이라이트"],
    ["코드 재계산", "매출성장률·영업이익률·부채비율 등을 LLM이 아닌 코드로 재계산해 원문 수치와 대조"],
    ["뉴스-공시 충돌 탐지", "뉴스 주장이 공시와 다르면 충돌로 표시"],
    ["확인 불가 처리", "근거 없는 문장은 삭제하지 않고 '확인 불가'로 명시"],
], [2, 9], size=10.5, row_h=380000)
add_text(s, X0, Y1 - 330000, W, 300000, [
    ("p", "출처 연결은 기존 서비스에도 있음. 차별점은 코드 재계산·충돌 탐지·확인 불가 표기와 DART 특화. 경쟁사 비공개 기능은 단정하지 않음")], 10)

# ---------- 5. Agent 역할 및 Workflow ----------
s = slides[4]
remove_guide(s)
Y0 = Y0 + 90000
add_flow(s, X0, Y0, W, 420000, ["Planner", "Collector", "Analyst", "Verifier", "Reporter"], 11)
add_text(s, X0, Y0 + 450000, W, 260000, [
    ("p", "Verifier가 근거 부족·수치 불일치를 발견하면 Collector로 되돌려 보완 수집(조건부 루프)")], 10)
add_table(s, X0, Y0 + 720000, W, [
    ["역할", "목표", "자율 판단·수행 범위"],
    ["Planner", "요청 분석, 대상 기업·비교 지표·수집 계획 수립", "기업명 식별, 지표 선택, 필요한 Tool 결정"],
    ["Collector", "OpenDART 공시·재무 API와 뉴스 수집", "누락 데이터 재조회, 실패 시 재시도"],
    ["Analyst", "Peer 비교, 지표 계산(코드), 주장 초안 생성", "비교 관점·핵심 차이 선별"],
    ["Verifier", "주장-출처 대조, 수치 재계산, 뉴스-공시 충돌 탐지", "검증됨/충돌/확인 불가 판정, 보완 수집 요청"],
    ["Reporter", "검증을 통과한 주장 중심으로 보고서 작성", "구조화·요약, 확인 불가 항목 명시"],
], [1.3, 4.5, 4.5], size=10, row_h=370000)
add_text(s, X0, Y0 + 720000 + 6 * 370000 + 40000, W, 560000, [
    ("b", "종료 조건: 모든 주장에 판정(검증됨/충돌/확인 불가)이 부여되면 종료. 보완 수집 루프는 최대 N회(예: 2회) 후 종료하고 남은 항목은 '확인 불가'"),
    ("b", "사용자 개입: 기업명이 모호하면 확인 질문"),
], 10)
Y0 = Y0 - 90000

# ---------- 6. AI 기술·Tool/API ----------
s = slides[5]
remove_guide(s)
add_text(s, X0, Y0, W, 900000, [
    ("b", "Framework: LangGraph(상태 그래프·조건부 루프). LLM은 제공자 추상화(LLMProvider)로 교체 가능, 모델 선정 기준: ① 수치·인용 과제 정확도 ② 비용 ③ 한국어 지원 ④ 교체 가능한 인터페이스. 후보 2~3개를 평가셋으로 비교해 확정"),
    ("b", "RAG·Memory: 수집한 공시·기사를 근거 단위(passage)로 저장·검색, 그래프 상태에 Claim Ledger 유지"),
], 10.5)
add_table(s, X0, Y0 + 640000, W, [
    ["Tool/API", "역할", "입력 → 출력", "호출 조건"],
    ["OpenDART 공시·재무 API", "재무제표·공시 조회", "기업, 기간 → 계정과목·접수번호", "Collector가 대상 기업별 호출"],
    ["뉴스 검색 API", "최근 이슈 수집", "기업명 → 기사 제목·URL·일자", "Collector가 호출"],
    ["재무 계산 Tool", "지표 재계산", "원본 수치 → 성장률·마진·부채비율", "Analyst·Verifier"],
    ["Claim Ledger", "주장-출처 연결 저장", "주장 → 출처 ID·판정", "모든 단계"],
], [2.2, 2.2, 3.6, 2.6], size=10, row_h=320000)
add_text(s, X0, Y0 + 640000 + 5 * 320000 + 40000, W, 1500000, [
    ("h", "신뢰성 확보 방안 (오류·환각 대응, 근거·출처 표시)"),
    ("b", "출처 없는 주장은 '확인 불가' 처리, 최종 보고서에 주장별 출처 표시"),
    ("b", "수치는 코드로 재계산하고 불일치 시 플래그, 뉴스-공시 충돌 표시"),
    ("b", "API 오류 시 재시도·부분 결과 보고(실패 사실 명시), 보완 수집 루프 횟수 제한"),
    ("b", "현재 구현: 저장소 MVP 골격에서 근거 ID 인용과 무근거 문장 제거를 합성 데이터로 시연"),
], 10)

# ---------- 7. 데이터 활용 계획 ----------
s = slides[6]
remove_guide(s)
add_table(s, X0, Y0, W, [
    ["데이터", "출처", "활용 목적", "수집·갱신", "전처리"],
    ["공시·재무제표", "OpenDART", "수치 근거 제시, 코드 재계산", "요청 시 조회, 캐시", "계정과목 정규화, 단위 통일"],
    ["뉴스", "샘플 뉴스(기본) + GDELT(선택, 출처 표기)", "이슈·리스크 파악, 공시 대조", "요청 시 조회", "중복 제거, 기업명 매칭"],
], [1.5, 3.6, 2.6, 1.9, 2.4], size=11.5, row_h=520000)
add_text(s, X0, Y0 + 1700000, W, 2200000, [
    ("h", "활용 방침"),
    ("b", "금융·기업·공시·뉴스 외부 데이터를 주장의 근거와 교차검증 용도로 활용 (산업 데이터는 확장 단계에서 검토)"),
    ("b", "데모는 소규모 공개 데이터 또는 합성 데이터만 사용하며 화면에 라벨 표시"),
    ("b", "출처·수집일·라이선스·전처리 방법은 외부 자원 기록표에 기록하고 부록과 일치시킴"),
    ("h", "확인 필요"),
    ("p", "OpenDART는 허용량이 홈페이지에 게시되며(약관 제10조) 분당 제한은 명시되지 않아 캐시·재시도로 대응, 공시 원문은 재배포하지 않고 DART 링크로 연결. 네이버 뉴스 API는 약관상 AI 입력 금지로 제외"),
], 13)

# ---------- 8. MVP 개발 계획 ----------
s = slides[7]
remove_guide(s)
add_text(s, X0, Y0, W, 900000, [
    ("b", "MVP 범위: 2~5개 기업 비교 · 주장별 출처 하이라이트 · 검증 요약(검증됨/충돌/확인 불가 건수)"),
    ("b", "개발 환경·스택: Python, LangGraph, FastAPI, Streamlit(또는 유사 UI), OpenDART"),
], 10.5)
add_table(s, X0, Y0 + 520000, W, [
    ["기간", "목표", "완료 기준"],
    ["11월 중순~하순", "OpenDART Collector, 재무 계산 Tool", "3개 기업 지표 재계산 일치"],
    ["12월 초", "Planner·Analyst·Verifier 그래프, Claim Ledger", "모든 주장에 판정 부여"],
    ["12월 중순", "UI(출처 하이라이트·검증 요약), 뉴스 충돌 탐지", "데모 시나리오 end-to-end 동작"],
    ["~12/22", "안정화, 실행 가이드·발표 자료, 데모 URL", "본선 제출물 완비"],
], [1.8, 5, 3.4], size=10, row_h=320000)
add_text(s, X0, Y0 + 520000 + 5 * 320000 + 40000, W, 1500000, [
    ("h", "데모 시나리오"),
    ("p", "\"A·B·C사 수익성·재무 안정성 비교\" → 보고서, 주장별 출처 하이라이트, 충돌 1건 표시, 확인 불가 문장 표시"),
    ("h", "주요 리스크와 대응"),
    ("b", "API 한도·장애 → 캐시·재시도  /  뉴스 데이터 확보 → 대체 소스·합성 샘플"),
    ("b", "기업명 매칭 오류 → 확인 질문  /  일정 지연 → 비교 기업을 2~3개로 축소"),
], 10)

# ---------- 9. 기대효과 및 확장성 ----------
s = slides[8]
remove_guide(s)
half = (W - 200000) // 2
add_text(s, X0, Y0, half, Y1 - Y0, [
    ("h", "기대효과"),
    ("b", "시간: 수집·정리 시간 단축"),
    ("b", "품질: 수치 오류 감소 (코드 재계산)"),
    ("b", "신뢰성: 주장별 출처 추적, 뉴스-공시 충돌과 확인 불가 항목의 투명한 표시"),
    ("b", "비용: 반복 리서치 업무의 인력 투입 감소"),
    ("p", "측정 목표: 동일 과제의 수작업 대비 작성 시간, 원문 대비 수치 불일치 건수, 주장별 출처 연결률을 MVP 파일럿에서 측정해 보고"),
], 14)
add_text(s, X0 + half + 200000, Y0, half, Y1 - Y0, [
    ("h", "향후 확장 가능성"),
    ("b", "해외 공시(EDGAR 등), 산업 리포트 연계"),
    ("b", "내부 문서·규정 검색 및 워크플로우 자동화"),
    ("b", "포트폴리오 모니터링, 정기 리포트 자동화"),
    ("h", "운영 적용 경로"),
    ("b", "소수 종목 파일럿 → 담당자 검토·승인 워크플로우 연계 → 내부 시스템 연동"),
], 14)

# ---------- 10. 부록 ----------
s = slides[9]
remove_guide(s)
add_table(s, X0, Y0, W, [
    ["구분", "이름", "출처", "이용 조건"],
    ["공시·재무 API", "OpenDART", "opendart.fss.or.kr", "금감원 약관·저작권법 준용 (2026-11-06 확인)"],
    ["뉴스 API", "GDELT(선택)", "gdeltproject.org", "자유 이용·재배포 가능, GDELT 출처·링크 표기 (2026-11-06 확인)"],
    ["오픈소스", "LangGraph", "github.com/langchain-ai/langgraph", "MIT (2026-11-06 확인)"],
    ["오픈소스", "FastAPI / Streamlit", "공식 저장소", "MIT / Apache-2.0 (2026-11-06 확인)"],
    ["데모 데이터", "합성 샘플", "자체 제작", "자체 저작물"],
], [1.6, 2.2, 3.4, 3.4], size=10, row_h=330000)
add_text(s, X0, Y0 + 6 * 330000 + 60000, W, 1800000, [
    ("h", "생성형 AI·AI 개발 도구 활용 내역"),
    ("p", "사용 모델명과 활용 범위:"),
    ("b", "도구: GitHub Copilot (사용 모델: Claude Sonnet 5.5, GPT-6 Astra)"),
    ("b", "활용 범위: 스캐폴딩, 기획서 초안 작성·수정, 아이디어 발굴·기획 보조, 출처 조사 보조, 코드·문서 생성"),
    ("h", "확인 사항"),
    ("b", "수집일·전처리 방법은 외부 자원 기록표와 일치시킬 것"),
    ("b", "민감정보·개인정보·API Key가 포함되지 않았는지 확인"),
], 10.5)

prs.save(OUT)
print("saved", OUT)

