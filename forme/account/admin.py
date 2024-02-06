from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "username",
        "email",
        "get_phone_number",
        "get_location",
        "get_date_of_birth",
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

    def get_phone_number(self, obj):
        if obj.phone_number:
            return obj.phone_number
        else:
            return "N/A"

    def get_location(self, obj):
        if obj.location:
            return obj.location
        else:
            return "N/A"

    def get_date_of_birth(self, obj):
        if obj.date_of_birth:
            return obj.date_of_birth
        else:
            return "N/A"

    def get_group(self, obj):
        return ", ".join(group.name for group in obj.groups.all())

    get_phone_number.short_description = "Phone"
    get_location.short_description = "Location"
    get_date_of_birth.short_description = "Data_of_Birth"
    get_group.short_description = "Group"


@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "get_username",
        "get_email",
        "get_phone",
        "get_group",
        "get_specialization",
    ]
    search_fields = [
        "user__username",
        "user__email",
    ]

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
        return ", ".join(group.name for group in obj.user.groups.all())

    def get_specialization(self, obj):
        if obj.specialization:
            return obj.specialization
        else:
            return "N/A"

    # save_model() is a overriden method from ModelAdmin class
    def save_model(self, request, obj, form, change):
        # Check if the "trainer" group exists
        trainer_group, created = Group.objects.get_or_create(name="trainers")

        # Add the user to the "trainer" group
        if not obj.user.groups.filter(name="trainer").exists():
            obj.user.groups.add(trainer_group)

        # Save the TrainerProfile instance
        super().save_model(request, obj, form, change)

    get_username.short_description = "Username"
    get_email.short_description = "Email"
    get_phone.short_description = "Phone"
    get_group.short_description = "Group"


@admin.register(TraineeProfile)
class TraineeProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "get_username",
        "get_email",
        "get_fitness_goals",
        "get_group",
        "get_current_fitness_level",
    ]
    search_fields = [
        "user__username",
        "user__email",
    ]

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_phone(self, obj):
        if obj.user.phone_number:
            return obj.user.phone_number
        else:
            return "N/A"

    def get_fitness_goals(self, obj):
        if obj.fitness_goals:
            return obj.fitness_goals
        else:
            return "N/A"

    def get_group(self, obj):
        return ", ".join(group.name for group in obj.user.groups.all())

    def get_current_fitness_level(self, obj):
        if obj.current_fitness_level:
            return obj.current_fitness_level
        else:
            return "N/A"

    # save_model() is a overriden method from ModelAdmin class
    def save_model(self, request, obj, form, change):
        # Check if the "trainer" group exists
        trainer_group, created = Group.objects.get_or_create(name="trainees")

        # Add the user to the "trainer" group
        if not obj.user.groups.filter(name="trainees").exists():
            obj.user.groups.add(trainer_group)

        # Save the TrainerProfile instance
        super().save_model(request, obj, form, change)

    get_username.short_description = "Username"
    get_email.short_description = "Email"
    get_phone.short_description = "Phone"
    get_group.short_description = "Group"


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = [
        "get_username",
        "get_email",
        "get_phone",
        "get_group",
    ]
    search_fields = [
        "user__username",
        "user__email",
    ]

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

    # save_model() is a overriden method from ModelAdmin class
    def save_model(self, request, obj, form, change):
        # Check if the "trainer" group exists
        trainer_group, created = Group.objects.get_or_create(name="owners")

        # Add the user to the "trainer" group
        if not obj.user.groups.filter(name="owners").exists():
            obj.user.groups.add(trainer_group)

        # Save the TrainerProfile instance
        super().save_model(request, obj, form, change)

    get_username.short_description = "Username"
    get_email.short_description = "Email"
    get_phone.short_description = "Phone"
    get_group.short_description = "Group"
