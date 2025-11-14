from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Resume
from django.core.exceptions import ObjectDoesNotExist

@shared_task
def send_resume_created_email(resume_id, user_email):
    try:
        resume = Resume.objects.get(id=resume_id)
    except ObjectDoesNotExist:
        return f"Resume {resume_id} not found. No email sent."
    
    subject = f"New Resume Created: {resume.title}"
    message = f"Hello,\n\nYour resume '{resume.title}' has been successfully created."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )