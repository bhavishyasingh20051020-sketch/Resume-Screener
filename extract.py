import re
import pypdf
from docx import Document


def extract_text_from_pdf(file):
    reader = pypdf.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return clean_text(text)


def extract_text_from_docx(file):
    doc = Document(file)
    text = "\n".join(p.text for p in doc.paragraphs)
    return clean_text(text)


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_resume_text(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX.")
