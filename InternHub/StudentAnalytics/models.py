from django.db import models

# Create your models here.

from django.core.exceptions import ValidationError

class StudentProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    skills = models.JSONField()
    interests = models.JSONField()
    projects = models.JSONField(blank=True)

    experience_summary = models.TextField(blank=True, null=True)

    # Resume inputs
    resume_file = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    resume_text = models.TextField(
        blank=True,
        null=True,
        help_text="Paste resume content or LaTeX code"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Ensure at least one of resume_file or resume_text is provided
        """
        if not self.resume_file and not self.resume_text:
            raise ValidationError("You must provide either a resume file or resume text.")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Internship(models.Model):
    company = models.CharField(max_length=100, db_index=True)
    role = models.CharField(max_length=100, db_index=True)

    description = models.TextField()
    required_skills = models.JSONField()

    location = models.CharField(max_length=100, blank=True, null=True)
    stipend = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.role}"

class MatchResult(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    version = models.PositiveIntegerField()

    match_summary = models.TextField()
    skill_gaps = models.JSONField()
    generated_resume = models.TextField()
    recommendation_text = models.TextField()
    ats_score = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("student", "internship", "version")
