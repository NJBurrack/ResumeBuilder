from rest_framework import serializers
from .models import Resume, Skill, JobHistory, EducationHistory


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'level']


class JobHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHistory
        fields = ['id', 'start_date', 'end_date', 'description', 'job_title']


class EducationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationHistory
        fields = ['id', 'institution', 'degree', 'start_date', 'end_date']


class ResumeSerializer(serializers.ModelSerializer):
    job_history = JobHistorySerializer(many=True)
    skills = SkillSerializer(many=True)
    education_history = EducationHistorySerializer(many=True)

    class Meta:
        model = Resume
        fields = [
            'id',
            'title',
            'bio',
            'address',
            'job_history',
            'skills',
            'education_history',
            'job_history_order',
            'skills_order',
            'education_history_order',
        ]

    def create(self, validated_data):
        job_history_data = validated_data.pop('job_history', [])
        skills_data = validated_data.pop('skills', [])
        education_data = validated_data.pop('education_history', [])

        resume = Resume.objects.create(**validated_data)

        for job in job_history_data:
            JobHistory.objects.create(resume=resume, **job)
        for skill in skills_data:
            Skill.objects.create(resume=resume, **skill)
        for edu in education_data:
            EducationHistory.objects.create(resume=resume, **edu)

        return resume

    def update(self, instance, validated_data):

        job_history_data = validated_data.pop('job_history', None)
        
        skills_data = validated_data.pop('skills', None)
        
        education_data = validated_data.pop('education_history', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        if skills_data is not None:
            instance.skills.all().delete()
            for skill in skills_data:
                Skill.objects.create(resume=instance, **skill)

        if job_history_data is not None:
            instance.job_history.all().delete()
            for job in job_history_data:
                JobHistory.objects.create(resume=instance, **job)

        if education_data is not None:
            instance.education_history.all().delete()
            for edu in education_data:
                EducationHistory.objects.create(resume=instance, **edu)

        return instance
