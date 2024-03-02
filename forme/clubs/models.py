from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify

from account.models import CustomUser, Trainee
from trainings.models import Review, Trainer


class Owner(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name": None},
        related_name="club_owner",
        primary_key=True,
    )

    def __str__(self):
        return f"{self.user.username}'s Club Owner"


class Club(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(
        Owner,
        on_delete=models.CASCADE,
        related_name="club_owner",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} Club"


class Branch(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    details = models.TextField(blank=True)
    working_hours = models.TextField(blank=True)
    trainers = models.ManyToManyField(
        Trainer,
        related_name="trainers_club",
        blank=True,
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="club_branches",
        null=True,
        blank=True,
    )
    location = models.CharField(max_length=255)
    members = models.ManyToManyField(
        Trainee,
        related_name="trainee_club",
        blank=True,
    )
    ratings = GenericRelation(
        Review,
        related_query_name="branch_ratings",
        null=True,
        blank=True,
    )
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = "%s %s" % (self.name, self.id)
            self.slug = slugify(slug_str)

        super(Branch, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )
    offer_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_plans",
        null=True,
        blank=True,
    )
    duration_in_months = models.PositiveIntegerField()
    # max trainees and current_trainees
    max_trainees_count = models.PositiveIntegerField(null=True, blank=True)
    current_trainees_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Facilities(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="club_facilities/")
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_facilities",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class ClubGallery(models.Model):
    galleries = models.ImageField(upload_to="club_galleries/")
    description = models.TextField(blank=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_gallery",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Club Gallery Image"
