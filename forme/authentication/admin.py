from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "id",
        "username",
        "email",
        "phone_number",
        "country",
        "date_of_birth",
        "get_group",
        "auth_provider",
    )

    search_fields = (
        "username",
        "email",
        "phone_number",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "email",
                    "date_of_birth",
                    "profile_picture",
                    "country",
                    "phone_number",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "Personal info",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def get_group(self, obj):
        return ", ".join(group.name for group in obj.groups.all())

    get_group.short_description = "Group"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "content_object",
        "latitude",
        "longitude",
    ]
    search_fields = [
        "content_object",
    ]


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
