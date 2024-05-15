from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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
            group_name="branches",
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
            username,
            email,
            password,
            group_name="admins",
            **extra_fields,
        )


AUTH_PROVIDER = {
    "facebook": "facebook",
    "google": "google",
    "email": "email",
    "twitter": "twitter",
}


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        default="profile_pics/default.png",
    )
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default="Male",
    )
    country = models.CharField(max_length=255, null=True, blank=True, default="Egypt")
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    auth_provider = models.CharField(
        max_length=255,
        default=AUTH_PROVIDER.get("email"),
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    def check_group(self, group_name):
        group_name = str(group_name + "s")
        return self.groups.filter(name=group_name).exists()

    def join_group(self, group_name):
        group = Group.objects.get(name=group_name)
        self.groups.add(group)
        self.save()

    def is_trainer(self):
        return self.groups.filter(name="trainers").exists()

    def is_trainee(self):
        return self.groups.filter(name="trainees").exists()

    def is_owner(self):
        return self.groups.filter(name="branches").exists()

    def is_admin(self):
        return self.groups.filter(name="admin").exists()

    def __str__(self):
        return (
            self.username + " " + ", ".join(group.name for group in self.groups.all())
        )


class Location(models.Model):
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
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
        return f"{self.longitude}, {self.latitude} - {self.content_object}'s Location"


class OTP(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    otp = models.IntegerField()
    validity = models.DateTimeField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# class Token(models.Model):
#     user = models.OneToOneField(
#         CustomUser,
#         on_delete=models.CASCADE,
#         related_name="tokens",
#     )
#     token = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username}'s Token"


# class ResetPasswordToken(models.Model):
#     user = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         related_name="password_reset_tokens",
#     )
#     token = models.CharField(max_length=5000)
#     created_at = models.DateTimeField()

#     def __str__(self):
#         return self.user.email
