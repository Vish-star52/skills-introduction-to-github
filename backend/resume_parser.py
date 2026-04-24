import os
import re
import tempfile
from typing import List

import PyPDF2
import spacy

SKILL_KEYWORDS = [
    "python", "flask", "react", "javascript", "sql", "machine learning", "nlp",
    "tensorflow", "pytorch", "scikit-learn", "data analysis", "aws", "docker",
    "kubernetes", "pandas", "numpy", "spark", "excel", "rest api", "git",
    "agile", "product management", "project management", "communication", "leadership"
]

nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(file_path: str) -> str:
    text = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text).strip()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_skills(text: str) -> List[str]:
    normalized = normalize_text(text)
    found = set()
    for skill in SKILL_KEYWORDS:
        if skill in normalized:
            found.add(skill.title())
    if not found:
        doc = nlp(text)
        for token in doc:
            if token.pos_ in {"NOUN", "PROPN"} and token.text.lower() in SKILL_KEYWORDS:
                found.add(token.text.title())
    return sorted(found)


def extract_summary(text: str) -> str:
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents][:3]
    return " ".join(sentences).strip()


def extract_resume_profile(text: str) -> dict:
    skills = extract_skills(text)
    summary = extract_summary(text)
    return {
        "text": text,
        "summary": summary,
        "skills": skills,
        "wordCount": len(text.split()),
        "experienceKeywords": [keyword for keyword in ["experience", "managed", "led", "developed", "designed"] if keyword in text.lower()]
    }
