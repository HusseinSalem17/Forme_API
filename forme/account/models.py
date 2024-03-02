from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group


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
    REQUIRED_FIELDS = ["username"]

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


# Create your models here.
class Trainee(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name": None},
        related_name="trainee_profile",
        primary_key=True,
    )
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    fitness_goals = models.TextField(blank=True)
    current_physical_level = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Trainee Profile"
