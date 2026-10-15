from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="JobProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("description", models.TextField(blank=True)),
                ("required_skills", models.TextField(help_text="Comma-separated job-related skills")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="CandidateAssessment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("candidate_name", models.CharField(max_length=160)),
                ("job_title", models.CharField(max_length=160)),
                ("cv_file", models.FileField(upload_to="candidate_cvs/")),
                ("cv_text", models.TextField(blank=True)),
                ("skill_matches", models.JSONField(blank=True, default=list)),
                ("nlp_analysis", models.JSONField(blank=True, default=dict)),
                ("ocean_scores", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
