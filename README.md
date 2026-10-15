# Ocean HR — AI-Assisted Recruitment Support

Ocean HR is a Django-based recruitment-support prototype designed to help HR teams review CVs against job requirements, examine relevant skill evidence, and prepare structured interview questions.

The project combines natural language processing (NLP), transparent skill matching, candidate assessment reports, and a voluntary OCEAN self-report questionnaire.

**Project status:** Working prototype under active development. Not yet ready for production recruitment use.

## Table of Contents

- [Features](#features)
- [AI and NLP Approach](#ai-and-nlp-approach)
- [Technology Stack](#technology-stack)
- [Installation on Windows](#installation-on-windows)
- [Running the Application](#running-the-application)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Limitations and Responsible Use](#limitations-and-responsible-use)
- [Planned Improvements](#planned-improvements)

## Features

### Implemented

- **HR dashboard:** View recent candidate assessments and assessment statistics.
- **Candidate assessment form:** Enter candidate details, job requirements, and a job description.
- **CV text extraction:** Extract text from PDF, DOCX, and TXT files, with an 8 MB upload limit.
- **Skill matching:** Compare listed job requirements with terms found in a CV.
- **Evidence snippets:** Display relevant CV text around matched skill terms.
- **Text similarity:** Compare CV text and job-description text using TF-IDF and cosine similarity.
- **Tailored interview questions:** Generate follow-up questions based on listed job skills and the available CV evidence.
- **OCEAN self-report questionnaire:** Record prototype scores across Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism.
- **Saved assessment reports:** Store candidate assessment data and retrieve previously saved reports.
- **Dashboard navigation:** Open an individual candidate's report by clicking the candidate name or job title in Recent Candidate Assessments.

### Planned Improvements

- A dedicated candidate-management page with search and filtering.
- More robust CV parsing, including improved handling of different document layouts.
- Better skill recognition, including synonyms and contextual evidence.
- Expanded HR analytics and downloadable reports.
- Authentication and role-based access controls.
- Stronger privacy, data-retention, and secure-file-management controls.
- Automated tests and deployment preparation.

Planned features are not represented as completed functionality.

## AI and NLP Approach

Ocean HR currently uses an explainable baseline rather than a trained hiring-prediction model.

### 1. CV text extraction

Text is extracted from supported document formats for subsequent analysis.

### 2. Job-related skill matching

Required skills are compared with the extracted CV text. The system records which terms were found and provides contextual evidence snippets.

A term match does not prove that a candidate possesses a skill or has the required proficiency.

### 3. TF-IDF and cosine similarity

TF-IDF converts text into numerical representations, and cosine similarity estimates lexical similarity between the CV and job description.

The resulting percentage is a text-similarity measure. It is **not** a probability of job success, a validated candidate score, or a hiring recommendation.

### 4. Interview-question generation

The system prepares questions based on the listed job skills, helping a human reviewer investigate experience, proficiency, and apparent evidence gaps.

### 5. OCEAN self-report

The prototype records questionnaire responses and calculates dimension scores. These scores are not produced by an AI model that infers personality from a CV.

The questionnaire and scoring approach have not been established as a validated psychometric instrument.

## Technology Stack

- **Language:** Python
- **Web framework:** Django
- **Database for local development:** SQLite
- **NLP and text similarity:** scikit-learn
- **PDF extraction:** pypdf
- **DOCX extraction:** python-docx
- **Frontend:** HTML, CSS, and Django templates
- **Version control:** Git and GitHub

## Installation on Windows

### Prerequisites

- Python compatible with the dependencies in `requirements.txt`
- Git
- Visual Studio Code

### 1. Clone the repository

Open PowerShell and run:

```powershell
git clone https://github.com/gyxxYc-newgyd-dinso3/ocean-hr-prototype.git
cd ocean-hr-prototype
```

### 2. Create a virtual environment

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can temporarily allow scripts in the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Apply database migrations

```powershell
python manage.py migrate
```

### 5. Create an administrator account (optional)

```powershell
python manage.py createsuperuser
```

### 6. Check the project configuration

```powershell
python manage.py check
```

## Running the Application

Start Django's development server:

```powershell
python manage.py runserver
```

Open the dashboard:

http://127.0.0.1:8000/

The Django administration interface is available at:

http://127.0.0.1:8000/admin/

The development server is intended for local development and testing, not public production deployment.

## How to Use

1. Open the dashboard.
2. Navigate to the candidate assessment form.
3. Enter the candidate's name and the job title.
4. Provide comma-separated required skills and a job description.
5. Upload a supported CV file.
6. Complete the prototype OCEAN questionnaire.
7. Submit the assessment.
8. Review the skill matches, evidence snippets, text-similarity measure, limitations, and tailored interview questions.
9. Return to Recent Candidate Assessments and click a candidate name or job title to reopen the saved report.

## Project Structure

```text
ocean-hr-prototype/
├── manage.py
├── oceanhr/
│   ├── settings.py
│   └── urls.py
├── recruitment/
│   ├── models.py
│   ├── views.py
│   ├── ai_engine.py
│   └── ocean.py
├── templates/
│   ├── dashboard.html
│   ├── assess.html
│   └── report.html
├── requirements.txt
├── README.md
└── .gitignore
```

This is a simplified overview of the main application files; additional project files may exist.

## Limitations and Responsible Use

Ocean HR is a decision-support prototype, not an automated hiring system.

- Skill matching relies on literal terms and may miss synonyms or equivalent experience.
- Text similarity can be affected by document quality, vocabulary, and formatting.
- CV extraction may fail or omit information in some documents.
- OCEAN scores are not validated personality or job-performance predictions.
- No claim of production readiness, GDPR compliance, psychometric validation, or independent bias auditing is made.
- Human reviewers must verify evidence, context, transferable skills, and candidate qualifications.
- Do not automatically rank, reject, or select applicants based on similarity or personality scores.
- Do not upload real candidate information to an unapproved or unsecured environment.

Before real recruitment use, the project needs appropriate authentication, access controls, secure file handling, retention and deletion procedures, audit logging, privacy and legal review, accessibility testing, and independent evaluation.

## Planned Improvements

The development roadmap includes:

1. Dedicated candidate-management and search functionality.
2. More robust, context-aware skill extraction.
3. Expanded analytics and reporting.
4. Automated testing and improved error handling.
5. Production security and privacy safeguards.
6. Further evaluation of AI methods before considering additional recruitment-related uses.

Contributions and suggestions for improving the prototype are welcome.
