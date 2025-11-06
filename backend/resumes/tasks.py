from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Resume

@shared_task
def send_resume_created_email(resume_id, recipient_email):
    resume = Resume.objects.get(id=resume_id)
    subject = f"New Resume Created: {resume.title}"
    message = f"Hello,\n\nYour resume '{resume.title}' has been successfully created."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=False,
    )

