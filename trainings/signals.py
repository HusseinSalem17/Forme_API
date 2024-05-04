from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Package, Trainer, Session, Availability
from datetime import time


@receiver(post_save, sender=Trainer)
def create_session_and_availability_and_package(sender, instance, created, **kwargs):
    if created:
        # Create Session
        session = Session.objects.create(trainer=instance)

        # Create Availability objects for each day of the week
        for day in Availability.DAY_CHOICES:
            Availability.objects.create(
                day=day[0],
                is_active=False,
                session=session,
            )

        for type in Package.SESSION_CHOICES:
            Package.objects.create(
                session_type=type[0],
                session=session,
            )
