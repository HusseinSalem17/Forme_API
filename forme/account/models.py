import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    def create_user(
        self, username, email, password=None, group_name=None, **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        user = self.model(username=username.strip(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return user

    def create_trainer(self, email, password=None, **extra_fields):
        return self.create_user(
            username="",  # Trainers don't have usernames
            email=email,
            password=password,
            group_name="trainers",
            **extra_fields,
        )

    def create_trainee(self, email, password=None, **extra_fields):
        return self.create_user(
            username="",  # Trainees don't have usernames
            email=email,
            password=password,
            group_name="trainees",
            **extra_fields,
        )

    def create_owner(self, username, email, password=None, **extra_fields):
        return self.create_user(
            username,
            email,
            password,
            group_name="owners",
            **extra_fields,
        )

    def create_admin(self, username, email, password=None, **extra_fields):
        return self.create_user(
            username,
            email,
            password,
            group_name="admins",
            **extra_fields,
        )

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            username, email, password, group_name="admins", **extra_fields
        )


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    username = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics",
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default="Male",
    )
    location = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def is_trainer(self):
        return self.groups.filter(name="trainers").exists()

    def is_trainee(self):
        return self.groups.filter(name="trainees").exists()

    def is_owner(self):
        return self.groups.filter(name="owners").exists()

    def is_admin(self):
        return self.groups.filter(name="admin").exists()

    def __str__(self):
        return (
            self.username + " " + ", ".join(group.name for group in self.groups.all())
        )


class TraineeProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name": None},
        related_name="trainee_profile",
        primary_key=True,
    )
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    fitness_goals = models.TextField(blank=True)
    current_fitness_level = models.CharField(max_length=255, blank=True)
    trainers = models.ManyToManyField(
        CustomUser,
        related_name="trainees",
        limit_choices_to={"groups__name": "trainers"},
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}'s Trainee Profile"


class Rating(models.Model):
    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Link the Rating to the Trainee providing the rating
    trainee = models.ForeignKey(
        TraineeProfile,
        on_delete=models.CASCADE,
        related_name="trainee_ratings",
    )

    # Add a GenericForeignKey to link the Rating to the Trainer being rated
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.trainee.user.username}'s Rating on {self.content_type} {self.object_id}"

    def save(self, *args, **kwargs):
        # Check if a rating already exists for the same trainee and trainer combination
        existing_rating = Rating.objects.filter(
            trainee=self.trainee,
            content_type=self.content_type,
            object_id=self.object_id,
        ).first()

        if existing_rating:
            # Update the existing rating if needed or raise an error
            existing_rating.rating = self.rating
            existing_rating.comment = self.comment
            existing_rating.save()
        else:
            # No existing rating, proceed with the save
            super().save(*args, **kwargs)

    def clean(self):
        # Ensure that a trainee can only make one rating for the same trainer
        existing_ratings = Rating.objects.filter(
            trainee=self.trainee,
            content_type=self.content_type,
            object_id=self.object_id,
        ).exclude(id=self.id)

        if existing_ratings.exists():
            raise ValidationError(
                "A trainee can only make one rating for the same trainer."
            )

        # Check if the object_id exists in the related class
        if self.content_type is not None and self.object_id is not None:
            try:
                related_class = self.content_type.model_class()
                related_object = related_class.objects.get(pk=self.object_id)
            except related_class.DoesNotExist:
                raise ValidationError("The specified object does not exist.")


class TrainerProfile(models.Model):
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
    document_files = models.FileField(upload_to="certifications/", blank=True)
    id_card = models.FileField(upload_to="id_cards/", blank=True)
    background_image = models.ImageField(upload_to="background_images/", blank=True)
    trainees = models.ManyToManyField(
        CustomUser,
        related_name="trainers",
        limit_choices_to={"groups__name": "trainees"},
        blank=True,
    )
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
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    number_of_trainees = models.PositiveIntegerField(default=0)
    # Add GenericRelation to link TrainerProfile to Rating
    ratings = GenericRelation(Rating, related_query_name="trainer_ratings")

    def save(self, *args, **kwargs):
        # Generate a unique slug based on the trainer's username
        if not self.slug:
            slug_str = "%s %s" % (self.user.username, self.user.id)
            self.slug = slugify(self, slug_str)

        super(TrainerProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Trainer Profile"


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


class OTP(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    otp = models.IntegerField()
    validity = models.DateTimeField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Token(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="tokens",
    )
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Token"


class ResetPasswordToken(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )
    token = models.CharField(max_length=5000)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.user.email


