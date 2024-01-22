from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group



# Create your models here.
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

    def create_trainer(self, username, email, password=None, **extra_fields):
        return self.create_user(
            username, email, password, group_name="trainers", **extra_fields
        )

    def create_trainee(self, username, email, password=None, **extra_fields):
        return self.create_user(
            username, email, password, group_name="trainees", **extra_fields
        )

    def create_owner(self, username, email, password=None, **extra_fields):
        return self.create_user(
            username, email, password, group_name="owners", **extra_fields
        )

    def create_admin(self, username, email, password=None, **extra_fields):
        return self.create_user(
            username, email, password, group_name="admin", **extra_fields
        )

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            username, email, password, group_name="admin", **extra_fields
        )


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics",
        null=True,
        blank=True,
    )
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    def is_trainer(self):
        return self.groups.filter(name="trainers").exists()

    def is_trainee(self):
        return self.groups.filter(name="trainees").exists()

    def is_gym(self):
        return self.groups.filter(name="owners").exists()

    def is_admin(self):
        return self.groups.filter(name="admin").exists()

    def __str__(self):
        return (
            self.username + " " + ", ".join(group.name for group in self.groups.all())
        )


class TrainerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="trainer_profile"
    )
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=255)
    certification_files = models.FileField(upload_to="certifications/", blank=True)
    id_card = models.FileField(upload_to="id_cards/", blank=True)
    background_image = models.ImageField(upload_to="background_images/", blank=True)
    trainees = models.ManyToManyField(CustomUser, related_name="trainers", blank=True)

    def __str__(self):
        return f"{self.user.username}'s Trainer Profile"


class TraineeProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="trainee_profile",
    )
    fitness_goals = models.TextField(blank=True)
    current_fitness_level = models.CharField(max_length=255, blank=True)
    trainers = models.ManyToManyField(CustomUser, related_name="trainees", blank=True)

    def __str__(self):
        return f"{self.user.username}'s Trainee Profile"
