import json
import re
from pathlib import Path
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

JOB_PATH = Path(__file__).resolve().parent / "sample_jobs.json"
KEYWORD_CANDIDATES = [
    "python", "flask", "react", "javascript", "sql", "machine learning", "nlp",
    "data", "cloud", "api", "agile", "aws", "docker", "kubernetes", "pandas",
    "numpy", "spark", "tensorflow", "pytorch", "communication", "leadership",
    "project management", "product management", "testing", "microservices", "rest api"
]


def load_job_descriptions() -> List[dict]:
    with open(JOB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_job_keywords(text: str) -> List[str]:
    normalized = normalize_text(text)
    found = set()
    for keyword in KEYWORD_CANDIDATES:
        if keyword in normalized:
            found.add(keyword)
    return sorted(found)


def compute_similarity(resume_text: str, job_descriptions: List[dict]) -> List[dict]:
    documents = [resume_text] + [job["description"] for job in job_descriptions]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)
    resume_vector = tfidf_matrix[0:1]
    job_vectors = tfidf_matrix[1:]
    similarities = cosine_similarity(resume_vector, job_vectors)[0]
    results = []
    for job, score in zip(job_descriptions, similarities):
        ats_details = compute_ats_details(resume_text, job["description"], job["title"])
        results.append({
            "id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "description": job["description"],
            "matchScore": round(float(score) * 100, 2),
            "atsScore": ats_details["totalScore"],
            "atsDetails": ats_details,
        })
    return sorted(results, key=lambda item: item["matchScore"], reverse=True)


def compute_ats_details(resume_text: str, job_description: str, job_title: str) -> dict:
    resume_text_norm = normalize_text(resume_text)
    job_text_norm = normalize_text(job_description)
    job_keywords = extract_job_keywords(job_text_norm)
    matched_skills = [keyword for keyword in job_keywords if keyword in resume_text_norm]
    skill_coverage = len(matched_skills) / max(len(job_keywords), 1)

    resume_words = len(resume_text_norm.split())
    length_score = min(max(resume_words / 450.0, 0.2), 1.0)

    title_keywords = [token for token in normalize_text(job_title).split() if len(token) > 3]
    title_matches = sum(1 for token in title_keywords if token in resume_text_norm)
    title_alignment = title_matches / max(len(title_keywords), 1)

    action_phrases = ["managed", "led", "developed", "designed", "delivered", "built", "implemented"]
    action_count = sum(1 for phrase in action_phrases if phrase in resume_text_norm)
    action_score = min(action_count / len(action_phrases), 1.0)

    total_score = round(
        (skill_coverage * 0.5 + length_score * 0.25 + title_alignment * 0.15 + action_score * 0.1) * 100,
        2,
    )

    return {
        "requiredSkills": job_keywords,
        "matchedSkills": matched_skills,
        "skillCoverage": round(skill_coverage * 100, 2),
        "lengthScore": round(length_score * 100, 2),
        "titleAlignment": round(title_alignment * 100, 2),
        "actionVerbScore": round(action_score * 100, 2),
        "totalScore": total_score,
    }
