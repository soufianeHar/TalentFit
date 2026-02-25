import os
from PyPDF2 import PdfReader
from docx import Document
from nlp.job_extractor import build_job_data

# Bank MVP (à agrandir plus tard)
SKILL_BANK = [
    "python", "sql", "power bi", "machine learning",
    "deep learning", "excel", "tableau",
    "business intelligence", "data analysis"
]

def extract_text_from_pdf(path):
    text = ""
    reader = PdfReader(path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_job(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        raw_text = extract_text_from_pdf(path)
    elif ext == ".docx":
        raw_text = extract_text_from_docx(path)
    elif ext == ".txt":
        raw_text = extract_text_from_txt(path)
    else:
        raise ValueError("Unsupported file format")

    return build_job_data(raw_text, SKILL_BANK)