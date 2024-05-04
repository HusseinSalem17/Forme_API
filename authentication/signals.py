from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from clubs.models import Branch
from .models import CustomUser, Location


@receiver(post_save, sender=CustomUser)
def create_location_user(sender, instance, created, **kwargs):
    if created:
        Location.objects.create(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        )


@receiver(post_save, sender=Branch)
def create_location_branch(sender, instance, created, **kwargs):
    if created:
        Location.objects.create(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        )
