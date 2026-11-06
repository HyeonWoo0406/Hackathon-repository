import os
import sys

from pptx.enum.shapes import MSO_CONNECTOR

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_pptx.py")
src = open(BASE, encoding="utf-8-sig").read()
HEAD = src.split("# ---------- 3. 문제 정의")[0]
TAIL = "# ---------- 10. 부록" + src.split("# ---------- 10. 부록")[1]
exec(compile(HEAD, "head", "exec"), globals())

WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(0x2E, 0x7D, 0x32)
ORANGE = RGBColor(0xE6, 0x51, 0x00)
MID = RGBColor(0x7F, 0x7F, 0x7F)
PALE = RGBColor(0xF4, 0xF6, 0xFA)


def box(slide, x, y, w, h, lines, fill=NAVY, fg=WHITE, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE):
    """lines: [(text, size, bold)]"""
    shp = slide.shapes.add_shape(shape, Emu(x), Emu(y), Emu(w), Emu(h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    shp.shadow.inherit = False
    tf = shp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(45000)
    tf.margin_top = tf.margin_bottom = Emu(20000)
    tf.vertical_anchor = anchor
    for i, (t, sz, b) in enumerate(lines):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.alignment = align
        add_runs(par, t, sz, bold=b, color=fg)
    return shp


def arrow(slide, x1, y1, x2, y2, color=MID):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(x1), Emu(y1), Emu(x2), Emu(y2))
    c.line.color.rgb = color
    c.line.width = Pt(1.5)
    ln = c.line._get_or_add_ln()
    etree.SubElement(ln, qn("a:tailEnd")).set("type", "triangle")
    return c


def headline(slide, text):
    box(slide, X0, Y0 - 60000, W, 340000, [(text, 12.5, True)], fill=LIGHT, fg=NAVY, shape=MSO_SHAPE.RECTANGLE,
        align=PP_ALIGN.LEFT)


# ---------- 3. 문제 정의 + 페르소나 ----------
s = slides[2]
remove_guide(s)
headline(s, "핵심 문제: 투자 리서치에는 빠른 요약보다 '검증 가능한' 비교가 필요하다")
px, py, pw, ph = X0, Y0 + 400000, 3500000, 3650000
box(s, px, py, pw, 330000, [("사용자 페르소나 (가상 인물)", 11.5, True)], shape=MSO_SHAPE.RECTANGLE)
box(s, px, py + 330000, pw, ph - 330000, [
    ("김서연 (가명)", 15, True),
    ("증권사 리서치센터 반도체 담당 애널리스트", 12.5, True),
    ("업무: 실적 시즌마다 Peer 3~5개사의 수익성·재무 안정성을 비교해 코멘트 작성", 12.5, False),
    ("고충: 공시·재무제표·뉴스를 오가며 수치를 옮기고, 보고서 문장마다 근거를 다시 확인해야 함", 12.5, False),
    ("바라는 것: 근거가 연결되어 있어 믿고 검토만 하면 되는 비교 초안", 12.5, False),
], fill=PALE, fg=GRAY, line=MID, shape=MSO_SHAPE.RECTANGLE, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
cx = X0 + pw + 200000
cw = (W - pw - 200000 - 150000) // 2
cards = [
    ("정보 분산", "공시·재무제표·뉴스가 흩어져 수집·정리에 시간 소요"),
    ("수치 오류", "전사·계산 과정에서 오류 가능, 단위·기간·연결/별도 혼동"),
    ("출처 불명", "근거가 불명확한 문장이 보고서에 섞임"),
    ("환각 위험", "일반 LLM 요약은 그럴듯하지만 근거 없는 문장을 생성할 수 있음"),
]
for i, (h, b) in enumerate(cards):
    x = cx + (i % 2) * (cw + 150000)
    y = py + (i // 2) * 1350000
    box(s, x, y, cw, 330000, [(h, 11.5, True)], shape=MSO_SHAPE.RECTANGLE)
    box(s, x, y + 330000, cw, 900000, [(b, 12.5, False)], fill=PALE, fg=GRAY, line=MID,
        shape=MSO_SHAPE.RECTANGLE, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
box(s, cx, py + 2750000, W - pw - 200000, 900000, [
    ("검증 가설 (파일럿에서 측정)", 11.5, True),
    ("동일 과제(3개사 비교)를 수작업과 Agent로 수행해 작성 시간·수치 불일치 건수를 비교한다. 시장 규모는 공개 근거가 없어 다루지 않는다. 유사 서비스는 출처 인용을 이미 제공하므로 이 부분은 차별점으로 주장하지 않는다.", 11, False),
], fill=WHITE, fg=GRAY, line=NAVY, shape=MSO_SHAPE.RECTANGLE, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 4. 서비스 제안 및 차별성 ----------
s = slides[3]
remove_guide(s)
cw3 = (W - 2 * 330000) // 3
chips = [("입력", "기업 2~5개 + 분석 관점"), ("Agent 수행", "계획 → 수집 → 분석 → 검증"),
         ("결과물", "근거 연결 비교 보고서 + 검증 요약")]
for i, (h, b) in enumerate(chips):
    x = X0 + i * (cw3 + 330000)
    box(s, x, Y0 - 40000, cw3, 480000, [(h, 10, True), (b, 11, True)], fill=NAVY)
    if i < 2:
        arrow(s, x + cw3 + 40000, Y0 + 200000, x + cw3 + 290000, Y0 + 200000)
add_text(s, X0, Y0 + 520000, W, 300000, [("h", "한국 공시 특화 차별점 (공개 자료 기준 비교)")], 11)
add_table(s, X0, Y0 + 820000, W, [
    ["기능", "PeerCheck (본 제안)", "AlphaSense · Hebbia · Rogo (공개 자료 기준)"],
    ["DART 계정과목명 정규화", "회사마다 다른 계정명을 표준 지표로 매핑", "공개 자료에서 확인되지 않음"],
    ["연결/별도 재무제표 선택", "지표별 기준을 명시·고정하고 혼용 시 경고", "공개 자료에서 확인되지 않음"],
    ["단위·기간 불일치 탐지", "천원/백만원, 누적/분기, 결산월 차이를 자동 점검", "공개 자료에서 확인되지 않음"],
    ["수치 코드 재계산", "LLM이 아닌 코드로 재계산해 원문과 대조", "공개 자료에서 확인되지 않음"],
    ["뉴스-공시 충돌 탐지", "수치·일자·사건명의 명시적 불일치만 검토 큐로 전달", "공개 자료에서 확인되지 않음"],
    ["주장-출처 연결", "주장 단위 Claim Ledger", "이미 제공 (차별점 아님)"],
], [2.6, 5.2, 3.6], size=10, row_h=430000)
add_text(s, X0, Y1 - 280000, W, 280000, [
    ("p", "경쟁 서비스의 비공개 기능은 단정하지 않으며, 공개 페이지에서 확인되지 않은 항목을 그렇게 표기함")], 9.5)

# ---------- 5. Agent 구성: 아키텍처 ----------
s = slides[4]
remove_guide(s)
# 상단: 사용자 / UI / API
tw = 2100000
top = [("사용자 (애널리스트)", NAVY), ("Streamlit UI", NAVY), ("FastAPI 서버", NAVY)]
tx = [X0, X0 + 2600000, X0 + 5200000]
for (t, c), x in zip(top, tx):
    box(s, x, Y0 - 10000, tw, 380000, [(t, 11, True)], fill=c)
arrow(s, X0 + tw + 30000, Y0 + 180000, tx[1] - 30000, Y0 + 180000)
arrow(s, tx[1] + tw + 30000, Y0 + 180000, tx[2] - 30000, Y0 + 180000)
box(s, X0 + 7600000, Y0 - 10000, 2650000, 380000, [("결과: 보고서 + 검증 요약 + 검토 큐", 10, True)],
    fill=LIGHT, fg=NAVY, line=NAVY)
arrow(s, tx[2] + tw + 30000, Y0 + 180000, X0 + 7570000, Y0 + 180000)
# LangGraph 컨테이너
cy, ch = Y0 + 450000, 1650000
box(s, X0, cy, W, ch, [("", 9, False)], fill=None, line=NAVY, shape=MSO_SHAPE.RECTANGLE)
add_text(s, X0 + 40000, cy + 10000, 4000000, 260000, [("h", "LangGraph Agent (상태 그래프)")], 10)
nodes = [("Planner", "기업·지표·계획 수립"), ("Collector", "공시·뉴스 수집"), ("Analyst", "Peer 비교·지표 계산"),
         ("Verifier", "주장 검증·충돌 판정"), ("Reporter", "보고서·검증 요약")]
gap = 260000
nw = (W - 2 * 150000 - gap * 4) // 5
ny = cy + 330000
nxs = []
for i, (n, d) in enumerate(nodes):
    x = X0 + 150000 + i * (nw + gap)
    nxs.append(x)
    box(s, x, ny, nw, 650000, [(n, 11.5, True), (d, 9, False)], fill=NAVY if n != "Verifier" else GREEN)
    if i < 4:
        arrow(s, x + nw + 20000, ny + 325000, x + nw + gap - 20000, ny + 325000)
# 보완 수집 루프
ly = ny + 650000 + 130000
c1 = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(nxs[3] + nw // 2), Emu(ny + 650000), Emu(nxs[3] + nw // 2), Emu(ly))
c2 = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(nxs[3] + nw // 2), Emu(ly), Emu(nxs[1] + nw // 2), Emu(ly))
for c in (c1, c2):
    c.line.color.rgb = ORANGE
    c.line.width = Pt(1.5)
arrow(s, nxs[1] + nw // 2, ly, nxs[1] + nw // 2, ny + 650000, color=ORANGE)
add_text(s, nxs[1] + nw // 2 + 60000, ly + 20000, 5000000, 260000, [
    ("p", "근거 부족·수치 불일치 시 Collector로 복귀 (보완 수집 최대 2회)")], 9.5)
# 도구 / 저장소
ty = cy + ch + 330000
tools = [("OpenDART API", "공시·재무제표", NAVY), ("뉴스 메타데이터", "샘플 기본 · GDELT 선택", NAVY),
         ("재무 계산 Tool", "코드 재계산", NAVY), ("LLM Provider", "교체형 인터페이스", NAVY)]
tw4 = (W - 3 * 200000) // 4
for i, (t, d, c) in enumerate(tools):
    x = X0 + i * (tw4 + 200000)
    box(s, x, ty, tw4, 520000, [(t, 11, True), (d, 9, False)], fill=WHITE, fg=NAVY, line=NAVY)
    arrow(s, x + tw4 // 2, cy + ch + 20000, x + tw4 // 2, ty - 20000)
sy = ty + 520000 + 120000
box(s, X0, sy, W // 2 - 100000, 400000, [("Claim Ledger (주장-출처-판정, 그래프 상태에 유지)", 10.5, True)], fill=LIGHT, fg=NAVY, line=NAVY)
box(s, X0 + W // 2 + 100000, sy, W // 2 - 100000, 400000, [("근거 단위 저장·검색 (RAG) · 응답 캐시", 10.5, True)], fill=LIGHT, fg=NAVY, line=NAVY)
add_text(s, X0, sy + 420000, W, 520000, [
    ("p", "자율 판단: 지표 선택·도구 호출·보완 수집 여부는 Agent가 결정, 모든 주장에 판정이 부여되거나 루프 2회 후 종료. LLM 선정 기준: 수치·인용 정확도, 비용, 한국어 지원, 교체 가능성 (후보 2~3개를 평가셋으로 비교해 확정)")], 9.5)

# ---------- 6. Claim Ledger 명세 ----------
s = slides[5]
remove_guide(s)
add_text(s, X0, Y0 + 10000, W, 280000, [("h", "Claim Ledger: 보고서의 모든 문장을 주장 단위로 분해해 출처와 판정을 기록")], 11)
add_table(s, X0, Y0 + 260000, W, [
    ["주장 유형", "예시", "최소 출처 요건", "허용오차·판정 기준"],
    ["수치", "영업이익률, 부채비율, 매출 성장률", "OpenDART 계정과목(접수번호) 1건 이상 + 코드 재계산", "비율 ±0.1%p, 금액은 표기 단위 반올림 내 (설정값, 평가셋으로 조정)"],
    ["사실", "공시 여부, 사건, 일자", "공시 접수번호 또는 기사 URL 1건 이상 (공시 우선)", "일자·사건명 정확 일치"],
    ["해석", "'A사가 B사보다 수익성이 높다'", "근거가 되는 수치·사실 주장 2건 이상 연결", "근거 주장이 모두 검증됨일 때만 통과"],
], [1.3, 2.9, 4.0, 4.0], size=10, row_h=470000)
fy = Y0 + 260000 + 4 * 470000 + 150000
add_text(s, X0, fy - 20000, 6200000, 260000, [("h", "판정 상태 전이")], 10.5)
bw, bh = 1100000, 330000
fy2 = fy + 330000
box(s, X0, fy2 + 330000, bw, bh, [("초안", 10.5, True)], fill=MID)
arrow(s, X0 + bw + 20000, fy2 + 495000, X0 + bw + 230000, fy2 + 495000)
box(s, X0 + bw + 250000, fy2 + 330000, bw, bh, [("검증 중", 10.5, True)], fill=NAVY)
ox = X0 + 2 * bw + 700000
for k, (t, c) in enumerate([("검증됨", GREEN), ("충돌", ORANGE), ("확인 불가", MID)]):
    oy = fy2 + k * 400000
    box(s, ox, oy, bw, bh, [(t, 10.5, True)], fill=c)
    arrow(s, X0 + 2 * bw + 290000, fy2 + 495000, ox - 30000, oy + 165000)
box(s, ox + bw + 250000, fy2 + 400000, 1500000, bh, [("검토 큐 → 승인/기각", 10, True)], fill=WHITE, fg=ORANGE, line=ORANGE)
arrow(s, ox + bw + 20000, fy2 + 565000, ox + bw + 230000, fy2 + 565000, color=ORANGE)
add_text(s, X0, fy2 + 1230000, 6600000, 300000, [
    ("p", "확인 불가는 보완 수집 후 재검증(최대 2회), 출처 없는 주장은 최종 보고서에서 '확인 불가'로 표기")], 9.5)
box(s, X0 + 6900000, fy + 20000, W - 6900000, 1500000, [
    ("신뢰성 KPI: 인용 정확도", 11, True),
    ("= 연결된 출처가 주장을 실제로 뒷받침하는 주장 수 ÷ 전체 주장 수 (평가셋에서 사람이 판정)", 10, False),
    ("오류·환각 대응: 출처 없음→확인 불가, 불일치→플래그, API 오류→재시도·부분 결과와 실패 사실 명시", 10, False),
], fill=PALE, fg=GRAY, line=NAVY, shape=MSO_SHAPE.RECTANGLE, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)

# ---------- 7. 데이터 활용 계획 + 충돌 탐지 ----------
s = slides[6]
remove_guide(s)
add_table(s, X0, Y0 - 50000, W, [
    ["데이터", "출처·조건", "활용", "전처리"],
    ["공시·재무제표", "OpenDART (허용량은 홈페이지 게시, 분당 제한 명시 없음 → 캐시·재시도, 원문 재배포 없이 DART 링크)", "수치 근거, 코드 재계산", "account_id 정규화, 단위·기간 통일, 최신 정정본 기준([기재정정] 표기)"],
    ["뉴스 메타데이터", "샘플 뉴스(기본) + GDELT(선택, 출처·링크 표기). 네이버 뉴스 API는 약관상 제외", "공시 대조 (제목·URL·일자·도메인만, 본문 미수집)", "중복 제거, 기업명 매칭"],
], [1.5, 5.4, 3.0, 2.4], size=9.5, row_h=430000)
ry = Y0 - 50000 + 3 * 430000 + 110000
add_text(s, X0, ry, W, 280000, [("h", "뉴스-공시 충돌 탐지 규칙 (명시적 불일치만 대상)")], 10.5)
add_table(s, X0, ry + 280000, W, [
    ["규칙", "입력 필드 (뉴스 ↔ 공시)", "판정 예시 (가상 수치)"],
    ["① 수치", "제목·스니펫의 금액·비율 ↔ 재계산값(계정과목·단위·기간)", "'영업이익률 15%' vs 재계산 12.0% → 충돌"],
    ["② 일자", "기사 내 공시·발표일 ↔ 접수일(rcept_dt)", "'3월 5일 공시' vs 접수일 3월 7일 → 충돌"],
    ["③ 사건명", "제목의 사건 키워드(유상증자·합병 등) ↔ 보고서명", "관련 공시를 찾지 못함 → 판정불가(검토 큐)"],
], [1.0, 5.2, 4.2], size=9.5, row_h=400000)
fy = ry + 280000 + 4 * 400000 + 110000
fw = (W - 2 * 330000) // 3
for i, (t, c) in enumerate([("자동 판정: 일치 / 충돌 / 판정불가", NAVY), ("검토 큐: 충돌·판정불가는 자동 확정하지 않음", ORANGE),
                            ("담당자 승인·기각 (이력 저장)", GREEN)]):
    x = X0 + i * (fw + 330000)
    box(s, x, fy, fw, 400000, [(t, 10, True)], fill=c)
    if i < 2:
        arrow(s, x + fw + 40000, fy + 200000, x + fw + 290000, fy + 200000)

# ---------- 8. MVP: 데모 시나리오 + 화면 ----------
s = slides[7]
remove_guide(s)
lw = 5700000
box(s, X0, Y0 - 50000, lw, 300000, [("데모 시나리오: 반도체 3사 비교 (삼성전자 · SK하이닉스 · DB하이텍)", 10.5, True)],
    fill=NAVY, shape=MSO_SHAPE.RECTANGLE, align=PP_ALIGN.LEFT)
box(s, X0, Y0 + 260000, lw, 420000, [
    ("질문: \"세 회사의 최근 사업연도 수익성과 재무 안정성을 비교해줘\"", 10, True)],
    fill=LIGHT, fg=NAVY, shape=MSO_SHAPE.RECTANGLE, align=PP_ALIGN.LEFT)
steps = [
    ("① Planner", "지표(영업이익률·부채비율) 선정, 연결(CFS) 기준으로 고정"),
    ("② Collector", "OpenDART 재무제표 3사 + 뉴스 메타데이터 수집, 출처 링크 저장"),
    ("③ Verifier", "삼성전자 2025 연결: 43.6조 ÷ 333.6조 × 100 = 13.07% (OpenDART 실조회·재계산)"),
    ("④ 충돌 1건", "가상 기사 제목 '영업이익률 15%' ≠ 재계산 13.07% → 충돌, 검토 큐 (예시)"),
    ("⑤ 확인 불가 1건", "'점유율 1위 유지' 문장은 출처 없음 → 확인 불가로 표기"),
]
sy0 = Y0 + 740000
for i, (h, b) in enumerate(steps):
    y = sy0 + i * 410000
    box(s, X0, y, 1250000, 380000, [(h, 9.5, True)], fill=NAVY if i < 3 else (ORANGE if i == 3 else MID), shape=MSO_SHAPE.RECTANGLE)
    box(s, X0 + 1250000, y, lw - 1250000, 380000, [(b, 9.5, False)], fill=PALE, fg=GRAY,
        shape=MSO_SHAPE.RECTANGLE, align=PP_ALIGN.LEFT)
add_text(s, X0, sy0 + 5 * 410000 + 10000, lw, 300000, [
    ("p", "※ ③은 OpenDART 실조회 값(접수번호 20260310002820). ④·⑤의 기사·문장은 가상 예시")], 9)
# UI 목업
mx, mw = X0 + lw + 250000, W - lw - 250000
box(s, mx, Y0 - 50000, mw, 2900000, [("", 9, False)], fill=WHITE, line=NAVY, shape=MSO_SHAPE.RECTANGLE)
box(s, mx, Y0 - 50000, mw, 280000, [("PeerCheck · 검증 요약 (화면 예시)", 10, True)], fill=NAVY,
    shape=MSO_SHAPE.RECTANGLE, align=PP_ALIGN.LEFT)
cwid = (mw - 4 * 90000) // 3
for i, (t, c) in enumerate([("검증됨 12", GREEN), ("충돌 1", ORANGE), ("확인 불가 1", MID)]):
    box(s, mx + 90000 + i * (cwid + 90000), Y0 + 290000, cwid, 320000, [(t, 10, True)], fill=c)
rows_ui = [
    ("검증됨", GREEN, "삼성전자 영업이익률 13.07%", "출처: 접수번호 20260310002820 · 재계산 ✓"),
    ("충돌", ORANGE, "가상 기사 '영업이익률 15%'", "공시 재계산과 불일치 → 검토 대기"),
    ("확인 불가", MID, "'점유율 1위 유지'", "출처 없음"),
]
for i, (st, c, t, sub) in enumerate(rows_ui):
    y = Y0 + 700000 + i * 640000
    hl = RGBColor(0xFF, 0xF3, 0xE0) if st == "충돌" else PALE
    box(s, mx + 90000, y, mw - 180000, 580000, [("", 9, False)], fill=hl, line=c, shape=MSO_SHAPE.RECTANGLE)
    box(s, mx + 130000, y + 110000, 760000, 250000, [(st, 9, True)], fill=c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    add_text(s, mx + 930000, y + 20000, mw - 1050000, 540000, [("p", t), ("p", sub)], 9)
add_text(s, mx + 90000, Y0 + 2640000, mw - 180000, 200000, [("p", "※ 개수와 기사·문구는 예시, 삼성전자 수치는 실조회")], 8.5)
# 일정
dy = Y0 + 3150000
steps2 = [("11월 중~하순", "Collector·재계산 Tool"), ("12월 초", "그래프·Claim Ledger"),
          ("12월 중순", "UI·충돌 탐지"), ("~12/22", "안정화·제출물")]
dw = (W - 3 * 120000) // 4
for i, (a, b) in enumerate(steps2):
    box(s, X0 + i * (dw + 120000), dy, dw, 520000, [(a, 10, True), (b, 9.5, False)], fill=NAVY, shape=MSO_SHAPE.PENTAGON)
add_text(s, X0, dy + 540000, W, 560000, [
    ("p", "MVP 범위: 기업 2~5개 비교 · 주장별 출처 하이라이트 · 검증 요약. 스택: Python, LangGraph, FastAPI, Streamlit, OpenDART. 리스크: API 한도→캐시·재시도, 일정 지연→비교 기업을 3개로 축소")], 9.5)

# ---------- 9. 기대효과 · KPI · 확장성 ----------
s = slides[8]
remove_guide(s)
add_text(s, X0, Y0 + 10000, W, 280000, [("h", "목표 KPI (팀 설정 목표치, 파일럿 측정 후 조정)")], 11)
add_table(s, X0, Y0 + 230000, W, [
    ["지표", "정의", "목표"],
    ["출처 연결률", "최종 보고서 주장 중 출처가 연결된 비율", "100% (연결 불가 주장은 '확인 불가' 표기)"],
    ["인용 정확도", "연결된 출처가 주장을 실제로 뒷받침하는 비율 (사람 판정)", "95% 이상"],
    ["재계산 일치율", "코드 재계산값이 DART 원문 정답과 일치한 지표 비율", "95% 이상"],
    ["오류 탐지율", "평가셋에 주입한 오류(수치 변조·단위·연결/별도 혼동) 중 플래그한 비율", "90% 이상"],
    ["작성 시간 단축", "동일 과제(3개사 비교)의 수작업 대비 소요 시간", "50% 이상 단축"],
], [1.6, 6.2, 3.4], size=10, row_h=330000)
by = Y0 + 230000 + 6 * 330000 + 120000
half = (W - 200000) // 2
box(s, X0, by, half, 1550000, [
    ("평가셋과 비교 절차", 11.5, True),
    ("평가셋: 반도체 3사 × 지표 5종의 정답표(DART 원문에서 팀이 수기 확정) + 주입 오류 문장", 11, False),
    ("① 동일 과제를 수작업(시간 측정)과 Agent로 수행해 비교", 11, False),
    ("② 검증 단계를 뺀 LLM 요약과 PeerCheck의 오류·환각 문장 수 비교", 11, False),
    ("③ 3회 반복 실행의 평균으로 보고", 11, False),
], fill=PALE, fg=GRAY, line=NAVY, shape=MSO_SHAPE.RECTANGLE, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
box(s, X0 + half + 200000, by, half, 1550000, [
    ("확장성과 운영 적용 경로", 11.5, True),
    ("확장: 해외 공시(EDGAR 등) · 내부 문서·규정 검색 · 포트폴리오 모니터링 · 정기 리포트 자동화", 11, False),
    ("경로: 소수 종목 파일럿 → 담당자 검토·승인 워크플로우 → 내부 시스템 연동", 11, False),
    ("구조: Tool·LLM Provider를 교체 가능한 모듈로 분리", 11, False),
], fill=PALE, fg=GRAY, line=NAVY, shape=MSO_SHAPE.RECTANGLE, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

exec(compile(TAIL, "tail", "exec"), globals())


