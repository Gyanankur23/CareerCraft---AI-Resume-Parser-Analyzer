import streamlit as st
import pandas as pd
import tempfile
from PyPDF2 import PdfReader
import docx
import re

# --- Helper Functions ---

def extract_text(file):
    ext = file.name.split('.')[-1].lower()
    text = ""
    if ext == 'pdf':
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    elif ext == 'docx':
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif ext == 'txt':
        try:
            text = file.read().decode("utf-8")
        except UnicodeDecodeError:
            text = file.read().decode("latin-1")
    return text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def summarize_text(text):
    keywords = [
        "business", "strategy", "growth", "sales", "marketing", "leadership", "operations",
        "project", "management", "client", "revenue", "team", "performance", "data", "analytics",
        "finance", "innovation", "solution", "impact", "result", "delivery", "execution", "planning"
    ]
    words = clean_text(text).split()
    summary = []
    for word in words:
        if word in keywords and word not in summary:
            summary.append(word)
        if len(summary) >= 30:
            break
    return " ".join(summary)

# --- Streamlit UI ---

st.set_page_config(page_title="Business Resume Summarizer", layout="wide")
st.title(" Business-Focused Resume Summarizer")
st.markdown("Upload resumes to extract a concise 30-word summary highlighting business-relevant strengths.")

with st.sidebar:
    st.header("Upload Resumes")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_files:
    summaries = []
    for file in uploaded_files:
        text = extract_text(file)
        summary = summarize_text(text)
        summaries.append({"File": file.name, "Summary": summary})

    df = pd.DataFrame(summaries)
    st.subheader("Extracted Business Highlights")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(" Download Summary CSV", csv, file_name="business_resume_summary.csv")
else:
    st.info("Upload one or more resumes to generate business-focused summaries.")
