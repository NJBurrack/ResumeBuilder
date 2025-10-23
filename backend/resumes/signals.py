from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Resume
from .tasks import send_resume_created_email

@receiver(post_save, sender=Resume)
def notify_resume_created(sender, instance, created, **kwargs):
    if created:
        send_resume_created_email.delay(instance.id, instance.owner.email)
