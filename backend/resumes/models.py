from django.db import models

# Create your models here.



class Resume(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    skills = models.TextField()
    address = models.CharField(max_length=255)
    job_history = models.TextField()
    education_history = models.TextField()

    def __str__(self):
        return self.name
