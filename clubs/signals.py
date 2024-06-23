# signals.py

from datetime import datetime, timedelta
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from clubs.tasks import decrease_new_members
from trainings.models import Program, Review, Trainer, Workout
from .models import (
    Attendance,
    Branch,
    BranchMember,
    MemberSubscription,
    Subscription,
    SubscriptionPlan,
    WorkingHours,
)
from .threads import thread_local
from django.utils.timezone import now
from django.db.models import Avg


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
    # Check if the deletion is happening because of Subscription deletion
    if getattr(thread_local, "subscription_deleting", False):
        return  # Do not proceed if it's a Subscription deletion

    if getattr(thread_local, "branch_deleting", False):
        return
    subscription = instance.subscription
    if Subscription.objects.filter(pk=subscription.pk).exists():
        SubscriptionPlan.objects.create(
            duration=instance.duration,
            price=subscription.price * instance.duration,
            subscription=subscription,
        )


@receiver(post_save, sender=MemberSubscription)
def create_attendance(sender, instance, created, **kwargs):
    if created:
        if (
            instance.state == "active"
            and instance.start_date is not None
            and instance.end_date is not None
        ):
            # Ensure start_date and end_date are date objects
            start_date = instance.start_date
            end_date = instance.end_date
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            day_count = (end_date - start_date).days + 1
            for day_number in range(day_count):
                Attendance.objects.create(
                    day=start_date + timedelta(days=day_number),
                    member_subscription=instance,
                )


# @receiver(post_save, sender=BranchMember)
# def update_branch_members(sender, instance, created, **kwargs):
#     if created:  # Check if a new BranchMember instance was created
#         branch = instance.branch
#         branch.total_members += 1
#         branch.new_members += 1
#         branch.save()

#         # Schedule the decrease_new_members task to run one week later
#         decrease_new_members.apply_async((branch.id,), eta=now() + timedelta(weeks=1))


@receiver(post_save, sender=Review)
def update_ratings_on_review_save(sender, instance, **kwargs):
    content_type = instance.content_type
    object_id = instance.object_id
    model_class = content_type.model_class()

    if model_class in [Trainer, Workout, Program, Branch]:
        reviewed_object = model_class.objects.get(pk=object_id)
        reviews = Review.objects.filter(content_type=content_type, object_id=object_id)
        avg_rating = reviews.aggregate(Avg("ratings"))["ratings__avg"]
        num_ratings = reviews.count()

        reviewed_object.avg_ratings = avg_rating
        reviewed_object.number_of_ratings = num_ratings
        reviewed_object.save()


@receiver(post_delete, sender=Review)
def update_ratings_on_review_delete(sender, instance, **kwargs):
    content_type = instance.content_type
    object_id = instance.object_id
    model_class = content_type.model_class()

    if model_class in [Trainer, Workout, Program, Branch]:
        try:
            reviewed_object = model_class.objects.get(pk=object_id)
            reviews = Review.objects.filter(
                content_type=content_type, object_id=object_id
            )
            avg_rating = reviews.aggregate(Avg("ratings"))["ratings__avg"] or 0.0
            num_ratings = reviews.count()

            reviewed_object.avg_ratings = avg_rating
            reviewed_object.number_of_ratings = num_ratings
            reviewed_object.save()
        except model_class.DoesNotExist:
            # Handle the case where the reviewed object does not exist
            pass

@receiver(post_save, sender=Branch)
def create_working_hours_for_new_branch(sender, instance, created, **kwargs):
    if created:
        for day in WorkingHours.DAY_CHOICES:
            WorkingHours.objects.create(
                day=day[0],
                is_open=False,
                branch=instance
            )
