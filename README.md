# CareerCraft---AI-Resume-Parser-Analyzer

# Business Resume Summarizer

This is a lightweight, AI-inspired Streamlit app that extracts and summarizes key business-relevant insights from resumes. It uses dynamic keyword extraction (TF-IDF) to generate a concise 30-word summary for each uploaded resume—ideal for recruiters, hiring managers, and analysts.

## Features

- Upload multiple resumes in PDF, DOCX, or TXT format  
- Automatically extracts and cleans resume text  
- Uses TF-IDF to identify the top 30 keywords per resume  
- Displays natural-language summaries without NLP libraries  
- Fully deployable on Streamlit Cloud

## Requirements

Add the following to your `requirements.txt`:


streamlit>=1.28.0 pandas>=1.5.0 PyPDF2>=3.0.1 python-docx>=1.0.0 scikit-learn>=1.3.0


## How to Run Locally

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
streamlit run app.py


Deploy on Streamlit Cloud
Push your code to a public GitHub repository

Go to Streamlit Cloud

Click “New App” and select your repo

Set the file path to app.py

Deploy and share your app link

```

### File Structure 
```bash
├── app.py
├── requirements.txt
└── README.md
```

### Sample Output 
Resume: John_Doe.pdf  
Summary: strategy leadership operations project management client growth analytics performance innovation delivery planning execution business solution impact result marketing finance team revenue data



This project is designed for fast, intelligent resume analysis with zero setup friction. Perfect for business use cases where clarity and speed matter most.

