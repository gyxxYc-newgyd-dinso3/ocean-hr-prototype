from django.db import models

class JobProfile(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    required_skills = models.TextField(help_text='Comma-separated job-related skills')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class CandidateAssessment(models.Model):
    candidate_name = models.CharField(max_length=160)
    job_title = models.CharField(max_length=160)
    cv_file = models.FileField(upload_to='candidate_cvs/')
    cv_text = models.TextField(blank=True)
    skill_matches = models.JSONField(default=list, blank=True)
    nlp_analysis = models.JSONField(default=dict, blank=True)
    ocean_scores = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.candidate_name} — {self.job_title}'
