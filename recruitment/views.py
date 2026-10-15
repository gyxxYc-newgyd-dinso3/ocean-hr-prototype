from pathlib import Path
from pypdf import PdfReader
from docx import Document
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import CandidateAssessment
from .ocean import DIMENSIONS, INTERVIEW_QUESTIONS
from .ai_engine import analyse_cv_against_job, generate_job_interview_questions

MAX_UPLOAD = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

def extract_text(uploaded_file):
    ext = Path(uploaded_file.name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError('Please upload a PDF, DOCX, or TXT file.')
    if uploaded_file.size > MAX_UPLOAD:
        raise ValueError('File is too large. Maximum size is 8 MB.')
    if ext == '.pdf':
        reader = PdfReader(uploaded_file)
        return '\n'.join(page.extract_text() or '' for page in reader.pages)
    if ext == '.docx':
        doc = Document(uploaded_file)
        return '\n'.join(p.text for p in doc.paragraphs)
    return uploaded_file.read().decode('utf-8', errors='replace')

def match_skills(text, required_skills):
    # Transparent keyword baseline, not a trained or validated AI model.
    terms = [x.strip() for x in required_skills.split(',') if x.strip()]
    lower_text = text.casefold()
    return [{'skill': term, 'found': term.casefold() in lower_text} for term in terms]

def dashboard(request):
    from django.db.models import Count
    from django.db.models.functions import TruncMonth

    assessments = CandidateAssessment.objects.all()
    total_assessments = assessments.count()
    distinct_positions = (
        assessments.values('job_title').distinct().count()
    )

    skill_percentages = []
    for assessment in assessments.only('skill_matches').iterator():
        matches = assessment.skill_matches or []
        if matches:
            found_count = sum(
                1 for item in matches if item.get('found')
            )
            skill_percentages.append(
                found_count / len(matches) * 100
            )

    average_skill_match = (
        round(sum(skill_percentages) / len(skill_percentages), 1)
        if skill_percentages else None
    )

    monthly_activity = list(
        assessments.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    context = {
        'recent': assessments.order_by('-created_at')[:8],
        'total_assessments': total_assessments,
        'distinct_positions': distinct_positions,
        'average_skill_match': average_skill_match,
        'monthly_activity': monthly_activity,
    }

    return render(request, 'dashboard.html', context)

def assess_candidate(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('candidate_name', '').strip()
            job = request.POST.get('job_title', '').strip()
            required = request.POST.get('required_skills', '').strip()
            job_description = request.POST.get('job_description', '').strip()
            cv = request.FILES.get('cv_file')
            if not name or not job or not required or not cv:
                raise ValueError('Please complete all fields and upload a CV.')
            text = extract_text(cv)
            nlp_analysis, matches = analyse_cv_against_job(text, job_description, required)
            tailored_questions = generate_job_interview_questions(required, matches)
            scores = {}
            for dimension, prompts in DIMENSIONS.items():
                values = [int(request.POST.get(f'q_{dimension}_{i}', '0')) for i in range(len(prompts))]
                if any(v < 1 or v > 5 for v in values):
                    raise ValueError('Please answer every OCEAN questionnaire item using a score from 1 to 5.')
                scores[dimension] = round(sum(values) / len(values) * 20)
            assessment = CandidateAssessment.objects.create(
                candidate_name=name, job_title=job, cv_file=cv, cv_text=text[:50000],
                skill_matches=matches, nlp_analysis=nlp_analysis, ocean_scores=scores)
            return render(request, 'report.html', {
                'assessment': assessment, 'questions': INTERVIEW_QUESTIONS,
                'dimensions': DIMENSIONS,
                'matched_count': sum(1 for x in matches if x['found']),
                'skill_count': len(matches),
                'tailored_questions': tailored_questions,
            })
        except Exception as exc:
            messages.error(request, str(exc))
    return render(request, 'assess.html', {'dimensions': DIMENSIONS})

def assessment_detail(request, assessment_id):
    assessment = get_object_or_404(
        CandidateAssessment,
        pk=assessment_id
    )

    matches = assessment.skill_matches or []

    required_skills = ", ".join(
        item.get("skill", "")
        for item in matches
        if item.get("skill")
    )

    tailored_questions = generate_job_interview_questions(
        required_skills,
        matches
    )

    return render(request, "report.html", {
        "assessment": assessment,
        "questions": INTERVIEW_QUESTIONS,
        "dimensions": DIMENSIONS,
        "matched_count": sum(
            1 for item in matches if item.get("found")
        ),
        "skill_count": len(matches),
        "tailored_questions": tailored_questions,
    })
