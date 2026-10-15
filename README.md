# OCEAN HR — NLP Upgrade Prototype

A Django recruitment-support prototype with transparent CV text extraction, skill evidence checks, TF-IDF/cosine similarity between a CV and job description, a voluntary OCEAN self-report questionnaire, and structured interview prompts.

## Implemented in this package
- Django dashboard, candidate assessment form, and report
- PDF/DOCX/TXT text extraction (8 MB upload limit)
- Literal skill-term evidence matching
- TF-IDF + cosine similarity for CV/job-description text comparison (a lexical NLP baseline)
- Job-skill-based interview follow-up questions
- Voluntary OCEAN self-report and structured OCEAN interview prompts
- Experimental supervised personality-model training scaffold (not connected to the web workflow)

## Not implemented / not validated
- No trained Big Five personality model is included
- The web app does **not** infer personality from CVs
- TF-IDF similarity is not a transformer/LLM and does not prove candidate suitability
- No production security, GDPR compliance review, psychometric validation, or bias audit is provided

## Windows + VS Code setup
1. Extract this folder somewhere writable, e.g. `C:\Users\YOUR_USER\Projects\ocean_hr_prototype`.
2. In VS Code, choose **File → Open Folder** and open the folder containing `manage.py`.
3. Open **Terminal → New Terminal**. Confirm `dir` shows `manage.py` and `requirements.txt`.
4. Create a virtual environment: `py -m venv .venv`
5. Activate it in PowerShell: `.\.venv\Scripts\Activate.ps1`
   - If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.
6. Install dependencies: `python -m pip install --upgrade pip` then `pip install -r requirements.txt`.
7. Apply database migrations: `python manage.py migrate`.
8. Create an admin account: `python manage.py createsuperuser`.
9. Start the server: `python manage.py runserver`.
10. Open `http://127.0.0.1:8000/`; admin is at `http://127.0.0.1:8000/admin/`.

If you already have a database, back it up before changing migrations. If this is an older extracted copy, keep your existing project folder as a backup and test this upgraded copy separately first.

## How to demo the NLP feature
1. Click **New assessment**.
2. Enter a candidate name and role.
3. Enter comma-separated job skills.
4. Paste the job description in the new job-description field.
5. Upload a text-based PDF, DOCX, or TXT CV.
6. Complete the voluntary OCEAN self-report for the demo candidate.
7. Submit. The report shows literal skill evidence, a CV/job text-similarity percentage, its limitations, and skill-specific interview follow-ups.

The similarity number is only a text similarity signal. Do not treat it as a candidate score, ranking, hiring recommendation, or proof of competence.

## Experimental Big Five research scaffold
The file `research_tools/train_personality_model.py` is **not** used by the web application. It requires a CSV named `research_tools/consented_big_five_dataset.csv` with columns `cv_text, openness, conscientiousness, extraversion, agreeableness, neuroticism`. Only use appropriately licensed and consented data with validated labels. The script prints held-out mean absolute error and saves an experimental model. Compare it with a baseline, validate across relevant groups, and obtain research/legal review before considering any further use. Do not use its predictions to make employment decisions. No dataset or trained model is included.

## Responsible-use and production checklist
Before any real recruitment deployment, add authentication and role-based permissions, secure file storage, retention/deletion controls, audit logging, upload malware scanning, secrets management, deployment security settings, accessibility testing, privacy and legal review (including GDPR and applicable employment/AI rules), and independent validity/bias evaluation. Do not automatically reject, rank, or select applicants based on personality or similarity scores.
