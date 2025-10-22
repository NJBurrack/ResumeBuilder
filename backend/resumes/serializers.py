from rest_framework import serializers
from .models import Resume, Skill, JobHistory, EducationHistory



class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'skill_level']


class JobHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHistory
        fields = ['start_date', 'end_date', 'description', 'job_title']


class EducationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationHistory
        fields = ['id', 'name', 'qualification']




class ResumeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    job_history = JobHistorySerializer(many=True, read_only=True)
    education_history = EducationHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = ['id', 'name', 'bio', 'address', 'skills', 'job_history', 'education_history']
