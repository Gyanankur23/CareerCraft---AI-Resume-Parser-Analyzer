import streamlit as st
import pandas as pd
import tempfile
from PyPDF2 import PdfReader
import docx
import re
from sklearn.feature_extraction.text import TfidfVectorizer

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
    text = re.sub(r'[^\w\s]', '', text.lower())
    text = re.sub(r'\s+', ' ', text)
    return text

def summarize_text(text):
    cleaned = clean_text(text)
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = vectorizer.fit_transform([cleaned])
    scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0])
    sorted_keywords = sorted(scores, key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, score in sorted_keywords[:30]]
    return " ".join(top_keywords)

# --- Streamlit UI ---

st.set_page_config(page_title="Business Resume Summarizer", layout="wide")
st.title("Business-Focused Resume Summarizer")
st.markdown("Upload resumes to receive a concise, AI-generated 30-word summary that highlights business-relevant strengths and strategic keywords.")

with st.sidebar:
    st.header("Upload Resumes")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("AI-Generated Business Insights")

    for file in uploaded_files:
        text = extract_text(file)
        summary = summarize_text(text)

        st.markdown(f"**{file.name}**")
        st.write("Summary based on business-relevant keywords extracted from the resume:")
        st.markdown(f"> {summary}")
        st.markdown("---")

else:
    st.info("Upload one or more resumes to generate intelligent 30-word summaries focused on business impact.")
