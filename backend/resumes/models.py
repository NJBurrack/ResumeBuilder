from django.db import models
from django.contrib.auth import get_user_model



# Create your models here


User = get_user_model()

class Resume(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    name = models.CharField(max_length=100)
    bio = models.TextField()
    address = models.CharField(max_length=255)

class Skill(models.Model):
    resume = models.ForeignKey(Resume, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    skill_level = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

class JobHistory(models.Model):
    resume = models.ForeignKey(Resume, related_name='job_history', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    job_title = models.CharField(max_length=100)

class EducationHistory(models.Model):
    resume = models.ForeignKey(Resume, related_name='education_history', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
