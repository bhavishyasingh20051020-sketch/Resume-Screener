import streamlit as st
from extract import extract_resume_text
from matcher import get_match_score
from keywords import find_missing_keywords

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="centered")

st.title("📄 AI Resume Screener")
st.write("Upload your resume and paste a job description to see how well you match.")

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Paste Job Description", height=200)

if st.button("Analyze", type="primary"):
    if not resume_file or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description first.")
    else:
        with st.spinner("Analyzing..."):
            resume_text = extract_resume_text(resume_file)

            if not resume_text.strip():
                st.error("Couldn't read any text from that file. Try a different one.")
                st.stop()

            score = get_match_score(resume_text, jd_text)
            missing = find_missing_keywords(resume_text, jd_text, top_n=15)

        st.subheader("Match Score")
        st.progress(min(int(score), 100))
        st.metric("Match Percentage", f"{score}%")

        st.subheader("Missing Keywords")
        if missing:
            st.write("These terms frm the job description weren't found in your resume:")
            cols = st.columns(3)
            for i, kw in enumerate(missing):
                cols[i % 3].markdown(f"- **{kw}**")
        else:
            st.success("Your resume already covers all the key terms from this job description.")

        with st.expander("Show extracted resume text"):
            st.text(resume_text)
