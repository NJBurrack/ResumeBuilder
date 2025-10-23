from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_resume_created_email(resume_id, user_email):
    send_mail(
        'Resume Created',
        f'Your resume with ID {resume_id} was successfully created.',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
