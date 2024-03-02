from email.headerregistry import Group
from django.contrib import admin

from .models import (
    Availability,
    Package,
    Program,
    ProgramPlan,
    Session,
    Time,
    Trainer,
    Workout,
    WorkoutFile,
    Review,
)


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


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "sport_field",
        "bio",
    ]
    search_fields = [
        "user__username",
        "sport_field",
    ]
    list_filter = [
        "user__username",
        "sport_field",
    ]


@admin.register(WorkoutFile)
class WorkoutFileAdmin(admin.ModelAdmin):
    list_display = [
        "file_or_video",
        "title",
        "details",
    ]


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = [
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
        "number_of_files",
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
    readonly_fields = [
        "current_trainees_count",
        "avg_ratings",
        "number_of_ratings",
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
        "session_type",
        "is_active",
        "price",
    ]


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = [
        "day",
        "is_active",
    ]


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = [
        "from_time",
        "to_time",
        "day",
    ]
