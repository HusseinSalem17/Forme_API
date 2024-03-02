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
        "location",
        "date_of_birth",
        "get_group",
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
                    "location",
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


@admin.register(Trainee)
class TraineeProfileAdmin(admin.ModelAdmin):
    list_display = [
        "get_id",
        "get_username",
        "get_email",
        "fitness_goals",
        "get_group",
        "current_physical_level",
    ]
    search_fields = [
        "user__username",
        "user__email",
    ]

    def get_id(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_phone(self, obj):
        if obj.user.phone_number:
            return obj.user.phone_number
        else:
            return "N/A"

    def get_group(self, obj):
        if obj.user.groups.exists():
            return ", ".join(group.name for group in obj.user.groups.all())
        else:
            return "N/A"

    def save_model(self, request, obj, form, change):
        # Check if the "trainee" group exists
        trainee_group, created = Group.objects.get_or_create(name="trainees")

        # Add the user to the "trainee" group
        if not obj.user.groups.filter(name="trainees").exists():
            obj.user.groups.add(trainee_group)

        # Save the TraineeProfile instance
        super().save_model(request, obj, form, change)

    get_id.short_description = "ID"
    get_username.short_description = "Username"
    get_email.short_description = "Email"
    get_phone.short_description = "Phone"
    get_group.short_description = "Group"

    def get_form(self, request, obj=None, **kwargs):
        # Customize the form based on whether it's for adding or editing
        if obj is None:
            # Adding a new TraineeProfile
            self.exclude = []
        else:
            # Editing an existing TraineeProfile
            self.exclude = ["user"]
        return super().get_form(request, obj, **kwargs)
