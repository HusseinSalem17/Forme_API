from django.contrib import admin

from .models import Branch, Club, ClubGallery, Owner, Plan
from django.contrib.auth.models import Group


# Register your models here.


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = [
        "get_id",
        "get_username",
        "get_email",
        "get_phone",
        "get_group",
    ]
    search_fields = [
        "id",
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

    # save_model() is a overriden method from ModelAdmin class
    def save_model(self, request, obj, form, change):
        # Check if the "trainer" group exists
        trainer_group, created = Group.objects.get_or_create(name="owners")

        # Add the user to the "trainer" group
        if not obj.user.groups.filter(name="owners").exists():
            obj.user.groups.add(trainer_group)

        # Save the TrainerProfile instance
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        # Customize the form based on whether it's for adding or editing
        if obj is None:
            # Adding a new TrainerProfile
            self.exclude = []
        else:
            # Editing an existing TrainerProfile
            self.exclude = ["user"]
        return super().get_form(request, obj, **kwargs)

    get_id.short_description = "ID"
    get_username.short_description = "Username"
    get_email.short_description = "Email"
    get_phone.short_description = "Phone"
    get_group.short_description = "Group"


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "owner",
    ]
    search_fields = [
        "id",
        "name",
        "owner__username",
    ]
    list_filter = [
        "created_at",
    ]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
        "details",
        "working_hours",
        "is_open",
        "location",
    ]
    search_fields = [
        "id",
        "name",
        "location",
    ]
    list_filter = [
        "location",
        "created_at",
    ]
    readonly_fields = ["slug"]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "price",
        "offer_price",
        "branch",
        "duration_in_months",
        "current_trainees_count",
        "max_trainees_count",
    ]
    search_fields = [
        "id",
        "branch",
        "name",
    ]
    list_filter = [
        "price",
        "offer_price",
        "branch",
    ]


@admin.register(ClubGallery)
class ClubGalleryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "galleries",
        "branch",
        "description",
    ]
    search_fields = [
        "id",
        "branch",
    ]
    list_filter = [
        "branch",
    ]
