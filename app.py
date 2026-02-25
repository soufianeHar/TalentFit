import streamlit as st
import os
import tempfile
import pandas as pd
import pathlib
from ingestion.cv_reader import parse_cv
from ingestion.job_reader import parse_job
from core.hybrid_engine import compute_hybrid_score


st.set_page_config(page_title="TalentFit", layout="wide")

st.title("🚀 TalentFit - Internal CV Intelligence Platform")

st.markdown("AI-powered CV Ranking System (Hybrid: Rules + Semantic Matching)")

# ==========================
# Load internal CV database
# ==========================

cv_folder = "data/cvs"
internal_cvs = []

for filename in os.listdir(cv_folder):
    if filename.endswith(".txt") and filename != "job.txt":
        path = os.path.join(cv_folder, filename)
        cv_data = parse_cv(path)
        internal_cvs.append((filename, cv_data))


# ==========================
# Tabs
# ==========================

tab1, tab2 = st.tabs(["📝 Manual Job Entry", "📄 Upload Job File"])

job_data = None

# ====================================
# TAB 1 — Manual Structured Entry
# ====================================

with tab1:

    st.subheader("Enter Job Requirements")

    required_skills = st.text_input("Required Skills (comma separated)")
    nice_skills = st.text_input("Nice-to-have Skills (comma separated)")
    min_experience = st.number_input("Minimum Years of Experience", min_value=0, max_value=20, value=0)
    required_level = st.selectbox("Required Technical Level", ["junior", "intermediate", "senior"])
    required_languages = st.text_input("Required Languages (comma separated)")

    if st.button("Evaluate Candidates"):

        job_data = {
            "required_skills": [s.strip().lower() for s in required_skills.split(",") if s],
            "nice_to_have_skills": [s.strip().lower() for s in nice_skills.split(",") if s],
            "min_experience": min_experience,
            "required_level": required_level,
            "required_languages": [l.strip().lower() for l in required_languages.split(",") if l],
            "raw_text": required_skills + " " + nice_skills
        }


# ====================================
# TAB 2 — Upload Job File
# ====================================

with tab2:

    job_file = st.file_uploader(
    "Upload Job Description",
    type=["txt", "pdf", "docx"]
)

    if job_file:

        file_extension = pathlib.Path(job_file.name).suffix

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_job:
            tmp_job.write(job_file.read())
            job_path = tmp_job.name

        job_data = parse_job(job_path)

        if st.button("Evaluate Candidates (Uploaded Job)"):
            pass


# ====================================
# Evaluation Engine
# ====================================

if job_data:

    st.header("🏆 Top 5 Candidates")

    results = []

    for filename, cv_data in internal_cvs:
        result = compute_hybrid_score(cv_data, job_data)
        results.append((filename, result))

    results.sort(key=lambda x: x[1]["hybrid_score"], reverse=True)
    top_results = results[:5]

    # KPI
    avg_score = sum(r[1]["hybrid_score"] for r in results) / len(results)
    st.metric("Average Candidate Score", round(avg_score, 2))

    # Chart
    chart_data = pd.DataFrame({
        "CV": [r[0] for r in top_results],
        "Hybrid Score": [r[1]["hybrid_score"] for r in top_results]
    })

    st.bar_chart(chart_data.set_index("CV"))

    # Results display
    for rank, (cv_name, result) in enumerate(top_results, start=1):

        st.subheader(f"Rank #{rank} - {cv_name}")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rule Score", result["rule_score"])
        col2.metric("Semantic Score", result["semantic_score"])
        col3.metric("Hybrid Score", result["hybrid_score"])

        if result["hybrid_score"] >= 75:
            st.success("🟢 STRONG MATCH")
        elif result["hybrid_score"] >= 50:
            st.warning("🟡 REVIEW")
        else:
            st.error("🔴 REJECT")

        with st.expander("View Detailed Explanation"):
            st.json(result["details"])