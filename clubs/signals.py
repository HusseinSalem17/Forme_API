# signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Subscription, SubscriptionPlan


@receiver(post_save, sender=Subscription)
def create_subscription_plans(sender, instance, created, **kwargs):
    if created:
        for duration in range(1, 13):
            if not SubscriptionPlan.objects.filter(
                subscription=instance, duration=duration
            ).exists():
                print("reached here", duration)
                SubscriptionPlan.objects.create(
                    duration=duration,
                    price=instance.price * duration,
                    subscription=instance,
                )


@receiver(post_save, sender=Subscription)
def update_subscription_plans(sender, instance, created, **kwargs):
    if not created:
        # If an existing subscription is updated
        subscription_plans = SubscriptionPlan.objects.filter(subscription=instance)
        for plan in subscription_plans:
            if plan.is_added:
                pass
            else:
                plan.price = instance.price * plan.duration
                plan.save()


@receiver(post_delete, sender=SubscriptionPlan)
def recreate_subscription_plan(sender, instance, **kwargs):
    subscription = instance.subscription
    SubscriptionPlan.objects.create(
        duration=instance.duration,
        price=subscription.price * instance.duration,
        subscription=subscription,
    )
