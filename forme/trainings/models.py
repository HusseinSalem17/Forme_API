from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField

from account.models import CustomUser, Trainee


class Review(models.Model):
    ratings = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    comment = models.TextField(blank=True)

    # Link the reviews to the Trainee providing the reviews
    trainee = models.ForeignKey(
        Trainee,
        related_name="trainee_reviews",
        on_delete=models.CASCADE,
        null=True,
    )

    # Add a GenericForeignKey to link the reviews to the Trainer being rated
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainee.user.username}'s reviews on {self.content_type} {self.object_id}"

    def save(self, *args, **kwargs):
        # Check if a reviews already exists for the same trainee and trainer combination
        existing_reviews = Review.objects.filter(
            trainee=self.trainee,
            content_type=self.content_type,
            object_id=self.object_id,
        ).first()

        if existing_reviews:
            # Update the existing reviews if needed or raise an error
            existing_reviews.reviews = self.reviews
            existing_reviews.comment = self.comment
            existing_reviews.save()
        else:
            # No existing reviews, proceed with the save
            super().save(*args, **kwargs)

    def clean(self):
        # Ensure that a trainee can only make one reviews for the same trainer
        existing_reviews = Review.objects.filter(
            trainee=self.trainee,
            content_type=self.content_type,
            object_id=self.object_id,
        ).exclude(id=self.id)

        if existing_reviews.exists():
            raise ValidationError(
                "A trainee can only make one reviews for the same trainer."
            )

        # Check if the object_id exists in the related class
        if self.content_type is not None and self.object_id is not None:
            try:
                related_class = self.content_type.model_class()
                related_object = related_class.objects.get(pk=self.object_id)
            except related_class.DoesNotExist:
                raise ValidationError("The specified object does not exist.")


class Transformations(models.Model):
    before_picture = models.ImageField(upload_to="transformations_pictures/")
    after_picture = models.ImageField(upload_to="transformations_pictures/")
    details = models.TextField(blank=True)
    trainer = models.ForeignKey(
        "Trainer",
        on_delete=models.CASCADE,
        related_name="trainer_transformations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainee.user.username}'s Transformation"


# Create your models here.
class Trainer(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name": None},
        related_name="trainer_profile",
        primary_key=True,
    )
    slug = models.SlugField(unique=True, blank=True, null=True, editable=False)
    bio = models.TextField(blank=True)
    sport_field = models.CharField(
        max_length=255,
        blank=True,
    )
    is_active = models.BooleanField(default=False)
    document_files = models.FileField(upload_to="certifications/", blank=True)
    id_card = models.FileField(upload_to="id_cards/", blank=True)
    background_image = models.ImageField(upload_to="background_images/", blank=True)
    number_of_trainees = models.PositiveIntegerField(default=0)
    exp_injuries = models.BooleanField(default=False)
    physical_disabilities = models.BooleanField(default=False)
    experience = models.CharField(
        max_length=5,
        blank=True,
        null=True,
    )
    languages = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list,
    )
    trainees = models.ManyToManyField(
        Trainee,
        related_name="trainees",
        blank=True,
    )
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    # Add GenericRelation to link TrainerProfile to reviews
    avg_ratings = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=0.0,
    )
    number_of_ratings = models.PositiveIntegerField(default=0)
    reviews = GenericRelation(Review, related_query_name="trainer_reviews")

    def save(self, *args, **kwargs):
        # Generate a unique slug based on the trainer's username
        if not self.slug:
            slug_str = "%s %s" % (self.user.username, self.user.id)
            self.slug = slugify(slug_str)

        super(Trainer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Trainer"


class Program(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("both", "Both"),
    ]
    title = models.CharField(max_length=255)
    picture = models.ImageField(
        upload_to="program_pictures/",
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    level = models.CharField(
        max_length=255,
        blank=True,
    )
    method = models.CharField(
        max_length=255,
        blank=True,
    )
    target_gender = models.CharField(
        max_length=255,
        choices=GENDER_CHOICES,
        default="both",
    )
    min_age = models.PositiveIntegerField(default=18)
    max_age = models.PositiveIntegerField(default=99)
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="trainer_programs",
    )
    trainees = models.ManyToManyField(
        Trainee,
        related_name="trainee_programs",
        blank=True,
    )
    current_trainees_count = models.PositiveIntegerField(default=0)
    max_trainees_count = models.PositiveIntegerField(null=True, blank=True)
    # Add GenericRelation to link Program to reviews
    avg_ratings = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=0.0,
    )
    number_of_ratings = models.PositiveIntegerField(default=0)
    reviews = GenericRelation(
        Review,
        related_query_name="program_reviews",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProgramPlan(models.Model):
    duration_in_weeks = models.PositiveIntegerField()
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
    max_trainees = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="program_plans",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.program.title} - {self.duration_in_weeks} Weeks"


class Workout(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("both", "Both"),
    ]
    title = models.CharField(max_length=255)
    picture = models.ImageField(
        upload_to="workout_pictures/",
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    level = models.CharField(
        max_length=255,
        blank=True,
    )
    target_gender = models.CharField(
        max_length=255,
        choices=GENDER_CHOICES,
        default="both",
    )
    min_age = models.PositiveIntegerField(default=18)
    max_age = models.PositiveIntegerField(default=99)
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
    current_trainees_count = models.PositiveIntegerField(default=0)
    max_trainees_count = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="trainer_workouts",
    )
    trainees = models.ManyToManyField(
        Trainee,
        related_name="trainee_workouts",
        blank=True,
    )
    duration_in_minutes = models.PositiveIntegerField(default=0)
    number_of_files = models.PositiveIntegerField(default=0)
    # Add GenericRelation to link Workout to reviews
    avg_ratings = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=0.0,
    )
    number_of_ratings = models.PositiveIntegerField(default=0)
    reviews = GenericRelation(
        Review,
        related_query_name="trainee_reviews_workout",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainer.user.username} - {self.title}"


class WorkoutFile(models.Model):
    file_or_video = models.FileField(
        upload_to="workout_files/",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    details = models.TextField(
        null=True,
        blank=True,
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name="workout_videos_files",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Session(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("both", "Both"),
    ]
    trainer = models.OneToOneField(
        Trainer,
        on_delete=models.CASCADE,
        related_name="trainer_session",
    )
    duration = models.PositiveIntegerField(default=15)  # Duration in minutes
    target_gender = models.CharField(
        max_length=255,
        choices=GENDER_CHOICES,
        default="both",
    )
    min_age = models.PositiveIntegerField(default=18)
    max_age = models.PositiveIntegerField(default=99)
    update_body_measure = models.BooleanField(default=False)
    update_pref_lifestyle = models.BooleanField(default=False)
    attach_body_img = models.BooleanField(default=False)
    attach_med_report = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.trainer.user.username}'s Session Settings"


class Package(models.Model):
    MESSAGING = "Messaging"
    VOICE_CALL = "Voice Call"
    VIDEO_CALL = "Video Call"
    IN_PERSON = "In Person"

    SESSION_CHOICES = [
        (MESSAGING, "Messaging"),
        (VOICE_CALL, "Voice Call"),
        (VIDEO_CALL, "Video Call"),
        (IN_PERSON, "In Person"),
    ]

    session_type = models.CharField(max_length=255, choices=SESSION_CHOICES)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="session_packages",
    )


class Availability(models.Model):
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
    is_active = models.BooleanField(default=False)
    availablity = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
        related_name="trainer_avilablity",
        null=True,
    )

    def __str__(self):
        return f"{self.get_day_display()} - Active: {self.is_active}"


class Time(models.Model):
    from_time = models.TimeField()
    to_time = models.TimeField()
    day = models.ForeignKey(
        Availability,
        on_delete=models.CASCADE,
        related_name="session_times",
    )
