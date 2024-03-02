from django.contrib import admin

from .models import OTP, Token


# Register your models here.
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "otp",
        "validity",
        "verified",
    ]
    search_fields = [
        "email",
    ]
    list_filter = [
        "verified",
        "validity",
    ]


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "token",
        "created_at",
    ]
    search_fields = [
        "user__username",
        "user__email",
    ]
