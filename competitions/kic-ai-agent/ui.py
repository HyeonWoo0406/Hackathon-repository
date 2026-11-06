import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from app.agent import ResearchAgent  # noqa: E402

st.title("KIC 투자 리서치 에이전트 (MVP)")
query = st.text_input("리서치 요청", "알파반도체 베타전자 비교")
if st.button("분석") and query:
    r = ResearchAgent().run(query)
    st.caption(r["data_label"])
    st.subheader("보고서")
    st.write(r["report"] or "근거 부족으로 답변하지 않았습니다.")
    st.subheader("인용 근거")
    st.json(r["citations"])
    st.subheader("실행 과정(도구 호출)")
    st.json(r["trace"])
    for f in r["flags"]:
        st.warning(f)
