# app.py

# -------------------------------
# 📦 Imports
# -------------------------------
import os
import tempfile
import pandas as pd
import streamlit as st
from docx import Document
from PyPDF2 import PdfReader
from resume_utils import update_docx_resume, update_pdf_resume

# -------------------------------
# 📂 Paths and Constants
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sample_dataset.csv")

DEFAULT_COLUMNS = [
    "Job Code", "Job Applied", "Job Category", "Job Location",
    "Resume Name", "Applicant Name", "Email", "Duplicates", "Mobile Number",
    "Applicant Location", "LinkedIn Profile URL", "Source_1",
    "Primary Skills", "Current Company", "Current Job Title", "Experience",
    "Job Posting Country"
]

# -------------------------------
# 🔍 Load Dataset Safely
# -------------------------------
def load_data(path):
    """
    Load dataset from CSV. If file not found, return empty DataFrame with default columns.
    """
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame(columns=DEFAULT_COLUMNS)

# -------------------------------
# 🖥️ Streamlit App UI
# -------------------------------
st.title("📊 Job Dataset Viewer")
data = load_data(DATA_PATH)

if not data.empty:
    st.write("🔍 Sample data:")
    st.dataframe(data.head(10))
else:
    st.info("No dataset available.")

# -------------------------------
# ATS-Friendly Resume Generator
# -------------------------------
st.title("ATS-Friendly Resume Generator")

# Input fields
job_description = st.text_area("📝 Paste Job Description (comma separated skills)", height=200)
user_linkedin = st.text_input("LinkedIn URL (optional)")
user_github = st.text_input("GitHub URL (optional)")
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

# -------------------------------
# Process Uploaded Resume
# -------------------------------
if uploaded_file:
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # Parse JD skills into a list
        jd_skills = [s.strip() for s in job_description.split(",")] if job_description else []

        # Clean JD skills for ATS matching
        jd_skills_clean = [s.strip().lower() for s in jd_skills if s.strip()]

        # Update DOCX resume
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            output_file = update_docx_resume(
                tmp_path,
                skills=jd_skills,
                linkedin=user_linkedin,
                github=user_github
            )

        # Update PDF resume
        elif uploaded_file.type == "application/pdf":
            output_file = update_pdf_resume(
                tmp_path,
                skills=jd_skills,
                linkedin=user_linkedin,
                github=user_github
            )

        # Extract existing resume skills (optional: for ATS matching)
        # Assuming extract_resume_skills_with_ai is available from resume_utils
        from utils.parser import extract_resume_skills_with_ai
        resume_text = ""
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(tmp_path)
            resume_text = "\n".join([p.text for p in doc.paragraphs])
        elif uploaded_file.type == "application/pdf":
            reader = PdfReader(tmp_path)
            resume_text = "\n".join([page.extract_text() or "" for page in reader.pages])

        resume_skills = extract_resume_skills_with_ai(resume_text)
        resume_skills_clean = [s.strip().lower() for s in resume_skills if s.strip()]

        # Provide download button for updated resume
        with open(output_file, "rb") as f:
            st.download_button(
                "📄 Download ATS-Friendly Resume",
                f.read(),
                file_name=os.path.basename(output_file)
            )

        st.success("✅ Resume updated successfully!")

    except Exception as e:
        st.error(f"❌ Error: {e}")