from django.contrib import admin

from .models import Program, Workout


# Register your models here.
# @admin.register(Rating)
# class RatingAdmin(admin.ModelAdmin):
#     list_display = [
#         "rating",
#         "comment",
#         "created_at",
#         "trainee",
#         "content_object",
#     ]
#     search_fields = [
#         "trainee__user__username",
#         "content_type__model",
#     ]
#     list_filter = [
#         "content_type__model",
#         "trainee__user__username",
#         "rating",
#         "created_at",
#     ]


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "duration_in_minutes",
        "trainer",
    ]
    search_fields = [
        "title",
        "trainer__user__username",
    ]
    list_filter = [
        "trainer__user__username",
        "created_at",
    ]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "duration_in_weeks",
        "trainer",
    ]
    search_fields = [
        "title",
        "trainer__user__username",
    ]
    list_filter = [
        "trainer__user__username",
        "created_at",
    ]
