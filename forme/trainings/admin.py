from email.headerregistry import Group
from django.contrib import admin

from .models import (
    Availability,
    ClientRequest,
    Package,
    Payment,
    Program,
    ProgramPlan,
    Session,
    Time,
    Trainee,
    Trainer,
    Transformations,
    Workout,
    WorkoutFile,
    Review,
)


@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
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

    # def save_model(self, request, obj, form, change):
    #     # Check if the "trainee" group exists
    #     trainee_group, created = Group.objects.get_or_create(name="trainees")

    #     # Add the user to the "trainee" group
    #     if not obj.user.groups.filter(name="trainees").exists():
    #         obj.user.groups.add(trainee_group)

    #     # Save the TraineeProfile instance
    #     super().save_model(request, obj, form, change)

    get_id.short_description = "ID"
    get_username.short_description = "Username"
    get_email.short_description = "Email"
    get_phone.short_description = "Phone"
    get_group.short_description = "Group"


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = [
        "get_id",
        "user",
        "slug",
        "bio",
        "sport_field",
    ]
    search_fields = [
        "user__username",
        "sport_field",
    ]
    list_filter = [
        "user__username",
        "sport_field",
    ]
    readonly_fields = [
        "slug",
        "avg_ratings",
        "number_of_ratings",
        "number_of_trainees",
    ]

    def get_id(self, obj):
        return obj.user.id

    get_id.short_description = "ID"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "ratings",
        "comment",
        "created_at",
        "trainee",
        "content_object",
    ]
    search_fields = [
        "trainee__user__username",
        "content_type__model",
    ]
    list_filter = [
        "content_type__model",
        "trainee__user__username",
        "ratings",
        "created_at",
    ]


@admin.register(WorkoutFile)
class WorkoutFileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "file_or_video",
        "title",
        "details",
    ]


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "description",
        "duration_in_minutes",
        "trainer",
        "avg_ratings",
        "number_of_ratings",
    ]
    search_fields = [
        "title",
        "trainer__user__username",
    ]
    list_filter = [
        "trainer__user__username",
        "created_at",
    ]
    readonly_fields = [
        "number_of_videos",
        "duration_in_minutes",
        "current_trainees_count",
        "avg_ratings",
        "number_of_ratings",
    ]
    exclude = [
        "duration_in_minutes",
        "videos_count",
        "number_of_trainees",
        "number_of_videos",
        "avg_ratings",
        "number_of_ratings",
    ]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "description",
        "trainer",
        "avg_ratings",
        "number_of_ratings",
    ]
    search_fields = [
        "title",
        "trainer__user__username",
    ]
    list_filter = [
        "trainer__user__username",
        "created_at",
    ]
    exclude = [
        "number_of_trainees",
        "avg_ratings",
        "number_of_ratings",
    ]


@admin.register(ProgramPlan)
class ProgramPlanAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "duration_in_weeks",
        "price",
        "offer_price",
        "max_trainees",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "id",
        "duration_in_weeks",
        "price",
        "offer_price",
        "max_trainees",
    ]
    list_filter = [
        "price",
        "offer_price",
        "max_trainees",
        "created_at",
    ]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "trainer",
        "duration",
        "target_gender",
        "min_age",
        "max_age",
        "update_body_measure",
        "update_pref_lifestyle",
        "attach_med_report",
    ]


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "session_type",
        "is_active",
        "price",
    ]


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "day",
        "is_active",
    ]


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "from_time",
        "to_time",
        "availability",
    ]


@admin.register(Transformations)
class TransformationsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "file",
        "details",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "details",
    ]
    list_filter = [
        "created_at",
    ]
    readonly_fields = [
        "created_at",
    ]
    exclude = [
        "updated_at",
    ]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "trainee",
        "amount",
        "method",
        "status",
        "transaction_id",
        "content_type",
        "object_id",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "trainee__user__username",
        "transaction_id",
    ]

    list_filter = [
        "method",
        "status",
        "created_at",
    ]

@admin.register(ClientRequest)
class ClientRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "trainee",
        "program_plan",
        "message",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "trainee__user__username",
        "program_plan__id",
    ]
    list_filter = [
        "created_at",
    ]
