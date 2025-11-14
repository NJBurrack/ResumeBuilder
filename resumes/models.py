from django.db import models
from django.contrib.auth import get_user_model



# Create your models here


User = get_user_model()

class Resume(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100)
    bio = models.TextField()
    address = models.CharField(max_length=255)
    job_history_order = models.PositiveIntegerField(default=0)
    skills_order = models.PositiveIntegerField(default=1)
    education_history_order = models.PositiveIntegerField(default=2)

class JobHistory(models.Model):
    resume = models.ForeignKey(
        Resume, related_name="job_history", on_delete=models.CASCADE
    )
    job_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

class Skill(models.Model):
    resume = models.ForeignKey(
        Resume, related_name="skills", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=50, blank=True)

class EducationHistory(models.Model):
    resume = models.ForeignKey(
        Resume, related_name="education_history", on_delete=models.CASCADE
    )
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)