"""Explainable, job-related CV analysis for Ocean HR.

This is a transparent baseline, not a validated hiring prediction model.
It does not infer personality from CV text or make hiring decisions.
"""

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _normalise(text):
    """Normalise whitespace while preserving readable CV text."""
    return re.sub(r"\s+", " ", (text or "")).strip()


def _parse_required_skills(required_skills):
    """Accept comma-separated skills and remove empty or duplicate entries."""
    if isinstance(required_skills, str):
        values = required_skills.split(",")
    else:
        values = required_skills or []

    skills = []
    seen = set()

    for value in values:
        skill = _normalise(value)
        key = skill.casefold()

        if skill and key not in seen:
            skills.append(skill)
            seen.add(key)

    return skills


def _calculate_text_similarity(cv_text, job_description):
    """Return a lexical TF-IDF similarity percentage, or None if unavailable."""
    if not cv_text or not job_description:
        return None

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
        )

        matrix = vectorizer.fit_transform([cv_text, job_description])

        score = cosine_similarity(
            matrix[0:1],
            matrix[1:2],
        )[0][0]

        return round(float(score) * 100, 1)

    except ValueError:
        return 0.0


def analyse_cv_against_job(cv_text, job_description, required_skills):
    """Return skill evidence and an explainable job-match review.

    Skill coverage is the proportion of explicitly listed required skills
    whose terms appear in the CV. It does not measure proficiency.
    """
    cv = _normalise(cv_text)
    job = _normalise(job_description)
    skills = _parse_required_skills(required_skills)

    cv_lower = cv.casefold()
    matches = []
    evidence_snippets = []

    for skill in skills:
        skill_lower = skill.casefold()
        found = bool(skill_lower and skill_lower in cv_lower)

        matches.append({
            "skill": skill,
            "found": found,
        })

        if found:
            index = cv_lower.find(skill_lower)

            evidence_snippets.append({
                "skill": skill,
                "snippet": cv[
                    max(0, index - 90):
                    min(len(cv), index + len(skill) + 130)
                ].strip(),
            })

    matched_count = sum(
        1 for item in matches if item["found"]
    )
    missing_skills = [
        item["skill"] for item in matches if not item["found"]
    ]

    skill_coverage = (
        round(matched_count / len(matches) * 100, 1)
        if matches else None
    )

    text_similarity = _calculate_text_similarity(cv, job)

    # This is a descriptive review category, not a hiring recommendation.
    if skill_coverage is None:
        review_category = "Insufficient criteria"
        review_explanation = (
            "Add explicit job-related required skills before assessing coverage."
        )
    elif skill_coverage >= 80:
        review_category = "High listed-skill coverage"
        review_explanation = (
            "Most listed skill terms appear in the CV. "
            "Verify context, proficiency, and relevant experience."
        )
    elif skill_coverage >= 50:
        review_category = "Partial listed-skill coverage"
        review_explanation = (
            "Some listed skill terms appear in the CV. "
            "Review the evidence and clarify gaps with the candidate."
        )
    else:
        review_category = "Low listed-skill coverage"
        review_explanation = (
            "Few listed skill terms were found. "
            "Check for synonyms, transferable experience, and extraction errors "
            "before drawing conclusions."
        )

    analysis = {
        "method": "TF-IDF cosine similarity plus exact skill-term matching",
        "job_text_similarity_percent": text_similarity,
        "skill_coverage_percent": skill_coverage,
        "matched_skill_count": matched_count,
        "required_skill_count": len(matches),
        "missing_skills": missing_skills,
        "review_category": review_category,
        "review_explanation": review_explanation,
        "evidence_snippets": evidence_snippets,
        "limitations": [
            "This is decision support, not a validated hiring prediction model.",
            "Keyword matches do not prove skill proficiency or job suitability.",
            "A missing term does not prove that the candidate lacks the skill.",
            "Text similarity is not a probability of success in the job.",
            "Review CV extraction quality, synonyms, context, and transferable skills.",
            "OCEAN self-report scores are separate and do not affect this assessment.",
        ],
    }

    return analysis, matches


def generate_job_interview_questions(required_skills, skill_matches):
    """Generate job-related questions to verify evidence and clarify gaps."""
    skills = _parse_required_skills(required_skills)

    found = {
        item["skill"].casefold()
        for item in (skill_matches or [])
        if item.get("found")
    }

    questions = []

    for skill in skills:
        if skill.casefold() in found:
            question = (
                f"Tell me about a project where you used {skill}. "
                "What was your contribution, and what was the outcome?"
            )
            purpose = "Verify context, proficiency, contribution, and outcome."
        else:
            question = (
                f"What experience or training do you have with {skill}? "
                "Can you describe related or transferable experience?"
            )
            purpose = (
                "Clarify the apparent evidence gap without assuming "
                "the candidate lacks the skill."
            )

        questions.append({
            "skill": skill,
            "question": question,
            "purpose": purpose,
        })

    return questions
