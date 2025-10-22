from django.contrib import admin
from .models import Resume, Skill, JobHistory, EducationHistory

# Register your models here.


admin.site.register(Resume)

admin.site.register(Skill)

admin.site.register(JobHistory)

admin.site.register(EducationHistory)
