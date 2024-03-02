from django.db import models

from account.models import CustomUser


# Create your models here.
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
