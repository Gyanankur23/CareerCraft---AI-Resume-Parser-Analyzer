import streamlit as st
import pandas as pd
import spacy
import tempfile
from PyPDF2 import PdfReader
import docx
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

def extract_text(file):
    ext = file.name.split('.')[-1].lower()
    text = ""
    if ext == 'pdf':
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif ext == 'docx':
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif ext == 'txt':
        text = file.read().decode("utf-8")
    else:
        text = ""
    return text

def extract_entities(text):
    doc = nlp(text)
    email = ""
    phone = ""
    for token in doc:
        # Email
        if re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", token.text):
            email = token.text
        # Phone (basic)
        if re.match(r"\b\d{10}\b", token.text):
            phone = token.text
    # Skills extraction (basic: noun chunks)
    skills = list(set([chunk.text for chunk in doc.noun_chunks if len(chunk.text.split(" "))<4]))
    return {"email": email, "phone": phone, "skills": skills}

def flatten_results(results):
    rows = []
    for result in results:
        row = {
            "file_name": result['file_name'],
            "email": result['extracted_data']['email'],
            "phone": result['extracted_data']['phone'],
            "skills": ", ".join(result['extracted_data']['skills'])
        }
        rows.append(row)
    return pd.DataFrame(rows)

def cluster_skills(all_skills):
    # Flatten skills list
    skills_flat = [" ".join(skills) for skills in all_skills]
    vec = CountVectorizer()
    X = vec.fit_transform(skills_flat)
    kmeans = KMeans(n_clusters=min(3, len(skills_flat)), random_state=42, n_init='auto')
    labels = kmeans.fit_predict(X)
    return labels

st.set_page_config(page_title="Resume Parser & Analyzer", layout="wide")
st.title("📄 AI-Powered Resume Parser & Analyzer")
st.markdown("Upload multiple resumes (PDF, DOCX, or TXT) to extract emails, phone numbers, and skills. Analyze and cluster candidates with just a click!")

with st.sidebar:
    st.header("Upload Resumes")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_files:
    # Parse all resumes
    results = []
    progress = st.progress(0)
    for idx, file in enumerate(uploaded_files):
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_file_path = tmp_file.name
            file.seek(0)
            text = extract_text(file)
            entities = extract_entities(text)
            results.append({"file_name": file.name, "extracted_data": entities})
        progress.progress((idx+1)/len(uploaded_files))
    st.success(f"Processed {len(results)} files.")

    # Display results
    st.header("Parsing Results")
    df = flatten_results(results)
    st.dataframe(df)
    if st.button("Download CSV"):
        st.download_button("Download Results as CSV", df.to_csv(index=False), file_name="resume_results.csv")

    # Clustering skills
    all_skills = [r["extracted_data"]["skills"] for r in results]
    labels = cluster_skills(all_skills)
    df["Skill Cluster"] = labels
    st.subheader("Candidate Clusters by Skills")
    st.dataframe(df)

    # Visualization: Cluster Bar Chart
    st.bar_chart(df["Skill Cluster"].value_counts())

else:
    st.info("Upload one or more resumes to start parsing.")

st.markdown("""
---
**How to Use:**
1. Upload resumes in sidebar
2. View extracted info, clusters, and download results
""")
