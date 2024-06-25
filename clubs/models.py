from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator

from authentication.models import CustomUser
from clubs.threads import BranchDeletionContext, SubscriptionDeletionContext
from .utils import (
    get_upload_path_for_branch_gallery,
    get_upload_path_for_club_documents,
    get_upload_path_forl_club_icon_facility,
    get_upload_path_new_trainers,
)
from trainings.models import Program, Review, Trainee, Trainer, Workout

import random
from django.utils import timezone
from datetime import datetime


class Club(models.Model):
    property_name = models.CharField(max_length=255)
    club_website = models.URLField(null=True, blank=True)
    club_registration_number = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, default="Egypt")
    sport_field = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property_name} Club"


class Branch(models.Model):
    owner = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="branch_owner",
        unique=True,
    )
    current_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )
    total_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )
    slug = models.SlugField(unique=True, blank=True)
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="club_branches",
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    total_members = models.PositiveIntegerField(default=0)
    new_members = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)
    reviews = GenericRelation(
        Review,
        related_query_name="branch_ratings",
        null=True,
        blank=True,
    )
    avg_ratings = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=0.0,
    )
    number_of_ratings = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = "%s#%s" % (
                self.club.property_name,
                str(random.randint(1000, 9999)),
            )
            print("slug_str", slug_str)
            self.slug = slug_str.replace(" ", "-").lower()

        super(Branch, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with BranchDeletionContext():
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.club.property_name


class Document(models.Model):
    document = models.FileField(upload_to=get_upload_path_for_club_documents)
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="branch_documents",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.club.property_name


class Subscription(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("both", "Both"),
    ]
    title = models.CharField(max_length=255)
    target_gender = models.CharField(
        max_length=255,
        choices=GENDER_CHOICES,
        default="both",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )
    active = models.BooleanField(default=True)
    min_age = models.PositiveIntegerField(
        default=18,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
    )
    max_age = models.PositiveIntegerField(
        default=99,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_subscription",
    )
    is_completed = models.BooleanField(default=False)
    max_members = models.PositiveIntegerField(null=True, blank=True)
    current_members_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        with SubscriptionDeletionContext():
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


class SubscriptionPlan(models.Model):
    is_added = models.BooleanField(default=False)
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )
    is_offer = models.BooleanField(default=False)
    current_members_count = models.PositiveIntegerField(default=0)
    max_members = models.PositiveIntegerField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="subscription_plan",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.duration} months"

    class Meta:
        unique_together = ("duration", "subscription")


class NewTrainer(models.Model):
    email = models.EmailField()
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_new_trainer",
    )
    profile_picture = models.ImageField(
        upload_to=get_upload_path_new_trainers,
        default="profile_pics/default.png",
    )
    members_count = models.PositiveIntegerField(default=0)
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    subscriptions = models.ManyToManyField(
        Subscription,
        related_name="branch_new_trainer_subscription",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    unique_together = ("email", "branch")

    def __str__(self):
        return self.username


class BranchTrainer(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="branch_trainer",
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_trainer",
    )
    subscriptions = models.ManyToManyField(
        Subscription,
        related_name="branch_trainer_subscription",
        blank=True,
    )
    members_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("trainer", "branch")

    def __str__(self):
        return f"{self.trainer}"


class BranchMember(models.Model):
    trainee = models.ForeignKey(
        Trainee,
        on_delete=models.CASCADE,
        related_name="trainee_membership",
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_member",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("trainee", "branch")

    def __str__(self):
        return f"{self.trainee}"


class MemberSubscription(models.Model):
    STATE_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("suspend", "Suspend"),
    ]
    member = models.ForeignKey(
        BranchMember,
        on_delete=models.CASCADE,
        related_name="member_subscription",
    )
    trainer = models.OneToOneField(
        BranchTrainer,
        on_delete=models.DO_NOTHING,
        related_name="member_trainer",
        null=True,
        blank=True,
    )
    new_trainer = models.OneToOneField(
        NewTrainer,
        on_delete=models.DO_NOTHING,
        related_name="member_new_trainer",
        null=True,
        blank=True,
    )
    subscription_plan = models.OneToOneField(
        SubscriptionPlan,
        on_delete=models.DO_NOTHING,
        related_name="trainee_membership",
    )
    subscription = models.OneToOneField(
        Subscription,
        on_delete=models.DO_NOTHING,
        related_name="trainee_membership",
    )
    state = models.CharField(
        max_length=255,
        choices=STATE_CHOICES,
        default="suspended",
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} - {self.subscription_plan}"


class Attendance(models.Model):
    day = models.DateField()
    member_subscription = models.ForeignKey(
        MemberSubscription,
        on_delete=models.CASCADE,
        related_name="member_attendance",
    )
    date = models.TimeField(null=True, blank=True)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member_subscription} - {self.day}"

    class Meta:
        unique_together = ("day", "member_subscription")


class ContactUs(models.Model):
    message = models.TextField()
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_contact",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message}"


class WorkingHours(models.Model):
    DAY_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]
    day = models.CharField(max_length=255, choices=DAY_CHOICES)
    is_open = models.BooleanField(default=False)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="trainer_avilablity",
    )

    class Meta:
        unique_together = ("day", "branch")

    def __str__(self):
        return f"{self.get_day_display()} - Active: {self.is_open} - {self.branch}"


class Time(models.Model):
    from_time = models.TimeField()
    to_time = models.TimeField()
    day = models.ForeignKey(
        WorkingHours,
        on_delete=models.CASCADE,
        related_name="day_time",
    )
    
    # class Meta:
    #     unique_together = ("from_time", "to_time", "day")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        now = timezone.now().time()

        # Convert from_time and to_time from string to datetime.time if they are not already
        from_time_obj = (
            datetime.strptime(self.from_time, "%H:%M").time()
            if isinstance(self.from_time, str)
            else self.from_time
        )
        to_time_obj = (
            datetime.strptime(self.to_time, "%H:%M").time()
            if isinstance(self.to_time, str)
            else self.to_time
        )

        if from_time_obj <= now <= to_time_obj:
            self.day.is_open = True
            self.day.branch.is_open = True
        else:
            self.day.is_open = False
            self.day.branch.is_open = False
        self.day.save()
        self.day.branch.save()


class Facilities(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to=get_upload_path_forl_club_icon_facility)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_facilities",
    )

    def __str__(self):
        return self.name


class BranchGallery(models.Model):
    gallery = models.ImageField(upload_to=get_upload_path_for_branch_gallery)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_gallery",
    )

    def __str__(self):
        return f"Club Gallery Image: {self.branch}"


class TraineeWishList(models.Model):
    trainee = models.OneToOneField(
        Trainee,
        on_delete=models.CASCADE,
        related_name="trainee_wishlist_user",
    )
    workouts_wishlist = models.ManyToManyField(
        Workout,
        related_name="trainee_wishlist_workouts",
        blank=True,
    )
    programs_wishlist = models.ManyToManyField(
        Program,
        related_name="trainee_wishlist_programs",
        blank=True,
    )
    trainers_wishlist = models.ManyToManyField(
        Trainer,
        related_name="trainee_wishlist_trainers",
        blank=True,
    )
    club_wishlist = models.ManyToManyField(
        Club,
        related_name="trainee_wishlist_clubs",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.trainee}"
