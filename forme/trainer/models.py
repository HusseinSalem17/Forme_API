# from django.db import models



# # Create your models here.

# class Rating(models.Model):
#     RATING_CHOICES = [
#         (1, "1 Star"),
#         (2, "2 Stars"),
#         (3, "3 Stars"),
#         (4, "4 Stars"),
#         (5, "5 Stars"),
#     ]

#     trainee = models.ForeignKey(
#         Trainee,
#         on_delete=models.CASCADE,
#         related_name="ratings",
#     )
#     rating = models.IntegerField(choices=RATING_CHOICES)
#     comment = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.trainee.user.username} - {self.rating} Stars"


# class Program(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     duration_in_weeks = models.PositiveIntegerField()
#     trainer = models.ForeignKey(
#         Trainer,
#         on_delete=models.CASCADE,
#         related_name="trainer_programs",
#     )
#     trainees = models.ManyToManyField(
#         Trainee,
#         related_name="trainee_programs",
#         blank=True,
#     )
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=0.0,
#     )
#     ratings = models.ManyToManyField(
#         Rating,
#         related_name="program_ratings",
#         blank=True,
#     )
#     offer_price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True,
#     )
#     max_trainees = models.PositiveIntegerField()
#     current_trainees = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return self.title


# class Workout(models.Model):
#     title = models.CharField(max_length=255)
#     trainer = models.ForeignKey(
#         Trainer,
#         on_delete=models.CASCADE,
#         related_name="trainer_workouts",
#     )
#     videos = models.FileField(
#         upload_to="workout_videos/",
#         null=True,
#         blank=True,
#     )
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=0.0,
#     )
#     offer_price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True,
#     )
#     ratings = models.ManyToManyField(
#         Rating,
#         related_name="workout_ratings",
#         blank=True,
#     )
#     number_of_videos = models.PositiveIntegerField(default=0)
#     description = models.TextField()
#     duration_in_minutes = models.PositiveIntegerField()
#     videos_count = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.trainer.user.username} - {self.title}"
