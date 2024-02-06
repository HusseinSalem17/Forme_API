from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from account.models import Owner, Rating, TraineeProfile, TrainerProfile, CustomUser
from django.utils.text import slugify



class ClubGallery(models.Model):
    galleries = models.ImageField(upload_to="club_galleries/")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Club Gallery Image"


# override trainees to be the same in dashboard (like number days of membership , trainer, which subscription, start member and end member)
class Club(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    details = models.TextField(blank=True)
    working_hours = models.TextField(blank=True)
    facilities = models.TextField(blank=True)
    trainers = models.ManyToManyField(
        TrainerProfile, related_name="club_trainers", blank=True
    )
    members = models.ManyToManyField(
        TraineeProfile, related_name="trainee_club", blank=True
    )
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name="club_owner"
    )
    galleries = models.ManyToManyField(
        ClubGallery, related_name="club_galleries", blank=True
    )
    ratings = GenericRelation(Rating, related_query_name="club_ratings")
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Club, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# check of club and branch (more than branch show the drop list or not)
# check subscription OR membership (sentence), check all sentences is the same or what
class Branch(models.Model):
    name = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="branches")
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} - {self.club.name} Branch"


class Plan(models.Model):
    name = models.CharField(max_length=255)
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
    duration_in_months = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    # max trainees and current_trainees

    def __str__(self):
        return self.name
