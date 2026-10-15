# Experimental Big Five dataset format

To run `train_personality_model.py`, place `consented_big_five_dataset.csv` in this folder. Required columns:

- `cv_text` — text with a lawful basis to process and explicit research consent where required
- `openness`, `conscientiousness`, `extraversion`, `agreeableness`, `neuroticism` — numeric validated Big Five scores using a consistent documented scale

Do not fabricate labels or treat job titles, seniority, writing style, or demographics as ground-truth personality. Use validated assessments, documented consent, appropriate data governance, and a representative dataset. This scaffold is not validated for real hiring.
