from django.db import models

from django.contrib.contenttypes.fields import GenericRelation

from account.models import TraineeProfile, TrainerProfile


class Program(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_in_weeks = models.PositiveIntegerField()
    trainer = models.ForeignKey(
        TrainerProfile,
        on_delete=models.CASCADE,
        related_name="trainer_programs",
    )
    trainees = models.ManyToManyField(
        TraineeProfile,
        related_name="trainee_programs",
        blank=True,
    )
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
    cupon = models.CharField(max_length=255, blank=True)
    # Add GenericRelation to link Program to Rating
    # ratings = GenericRelation(Rating, related_query_name="trainee_ratings")
    max_trainees = models.PositiveIntegerField()
    current_trainees = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Workout(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    trainer = models.ForeignKey(
        TrainerProfile,
        on_delete=models.CASCADE,
        related_name="trainer_workouts",
    )
    videos = models.FileField(
        upload_to="workout_videos/",
        null=True,
        blank=True,
    )
    number_of_videos = models.PositiveIntegerField(default=0)
    trainees = models.ManyToManyField(
        TraineeProfile,
        related_name="trainee_workouts",
        blank=True,
    )
    number_of_trainees = models.PositiveIntegerField(default=0)
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
    cupon = models.CharField(max_length=255, blank=True)
    # Add GenericRelation to link Workout to Rating
    # ratings = GenericRelation(Rating, related_query_name="trainee_ratings")
    duration_in_minutes = models.PositiveIntegerField()
    videos_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainer.user.username} - {self.title}"
