"""Lightweight NLP helpers for job-related CV analysis.

This module does not infer personality or make hiring recommendations.
The TF-IDF similarity score is a text-similarity signal, not a qualification
score and not evidence of candidate suitability.
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _normalise(text):
    return re.sub(r"\s+", " ", (text or "")).strip()


def analyse_cv_against_job(cv_text, job_description, required_skills):
    """Return explainable text-similarity and skill evidence.

    TF-IDF + cosine similarity provides a baseline semantic-ish lexical
    comparison. It does not understand synonyms as well as transformer models.
    """
    cv = _normalise(cv_text)
    job = _normalise(job_description)
    skills = [s.strip() for s in (required_skills or "").split(",") if s.strip()]
    matches = []
    cv_lower = cv.casefold()
    for skill in skills:
        found = skill.casefold() in cv_lower
        matches.append({"skill": skill, "found": found})

    score = None
    if cv and job:
        try:
            matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=5000).fit_transform([cv, job])
            score = round(float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0]) * 100, 1)
        except ValueError:
            score = 0.0

    # Evidence snippets are deliberately simple and traceable to CV text.
    snippets = []
    for skill in skills:
        if skill.casefold() in cv_lower:
            idx = cv_lower.find(skill.casefold())
            snippets.append({"skill": skill, "snippet": cv[max(0, idx-90):min(len(cv), idx+len(skill)+130)].strip()})

    return {
        "method": "TF-IDF + cosine similarity (lexical baseline)",
        "job_text_similarity_percent": score,
        "matched_skill_count": sum(1 for item in matches if item["found"]),
        "required_skill_count": len(matches),
        "evidence_snippets": snippets,
        "limitations": [
            "Text similarity is not a measure of competence or job suitability.",
            "Keyword absence does not prove a candidate lacks a skill.",
            "This baseline may miss synonyms, context, and skill proficiency.",
        ],
    }, matches


def generate_job_interview_questions(required_skills, skill_matches):
    """Create structured, job-related follow-up questions from skill evidence."""
    found = {x["skill"].casefold() for x in skill_matches if x.get("found")}
    questions = []
    for skill in [s.strip() for s in (required_skills or "").split(",") if s.strip()]:
        if skill.casefold() in found:
            questions.append({"skill": skill, "question": f"Tell me about a project where you used {skill}. What was your specific contribution and what was the outcome?", "purpose": "Verify context, contribution, and outcome."})
        else:
            questions.append({"skill": skill, "question": f"What experience or training do you have with {skill}? If you have not used it yet, how would you approach learning it?", "purpose": "Give the candidate an opportunity to clarify experience or transferable skills."})
    return questions
