from django.contrib import admin

from .models import (
    Attendance,
    Branch,
    BranchMember,
    BranchTrainer,
    Club,
    BranchGallery,
    ContactUs,
    Facilities,
    MemberSubscription,
    Subscription,
    SubscriptionPlan,
    Time,
    WorkingHours,
    NewTrainer,
)
from django.contrib.auth.models import Group


# Register your models here.


# @admin.register(Owner)
# class OwnerAdmin(admin.ModelAdmin):
#     list_display = [
#         "get_id",
#         "get_username",
#         "get_email",
#         "get_phone",
#         "get_group",
#     ]
#     search_fields = [
#         "id",
#         "user__username",
#         "user__email",
#     ]

#     def get_id(self, obj):
#         return obj.user.id

#     def get_username(self, obj):
#         return obj.user.username

#     def get_email(self, obj):
#         return obj.user.email

#     def get_phone(self, obj):
#         if obj.user.phone_number:
#             return obj.user.phone_number
#         else:
#             return "N/A"

#     def get_group(self, obj):
#         if obj.user.groups.exists():
#             return ", ".join(group.name for group in obj.user.groups.all())
#         else:
#             return "N/A"

#     # save_model() is a overriden method from ModelAdmin class
#     def save_model(self, request, obj, form, change):
#         # Check if the "trainer" group exists
#         trainer_group, created = Group.objects.get_or_create(name="branches")

#         # Add the user to the "trainer" group
#         if not obj.user.groups.filter(name="branches").exists():
#             obj.user.groups.add(trainer_group)

#         # Save the TrainerProfile instance
#         super().save_model(request, obj, form, change)

#     def get_form(self, request, obj=None, **kwargs):
#         # Customize the form based on whether it's for adding or editing
#         if obj is None:
#             # Adding a new TrainerProfile
#             self.exclude = []
#         else:
#             # Editing an existing TrainerProfile
#             self.exclude = ["user"]
#         return super().get_form(request, obj, **kwargs)

#     get_id.short_description = "ID"
#     get_username.short_description = "Username"
#     get_email.short_description = "Email"
#     get_phone.short_description = "Phone"
#     get_group.short_description = "Group"


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "property_name",
        "documents",
        "club_website",
        "club_registration_number",
        "sport_field",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "id",
        "property_name",
    ]
    list_filter = [
        "created_at",
    ]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "price",
        "branch",
        "current_members_count",
        "created_at",
    ]
    search_fields = [
        "id",
        "branch__name",
    ]
    list_filter = [
        "created_at",
    ]
    redaonly_fields = [
        "current_members_count",
    ]


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "duration",
        "price",
        "is_offer",
        "max_members",
        "is_added",
        "current_members_count",
        "expiration_date",
        "subscription",
    ]
    search_fields = [
        "id",
        "subscription",
        "duration",
    ]
    list_filter = [
        "subscription",
        "duration",
    ]
    readonly_fields = [
        "max_members",
    ]


@admin.register(NewTrainer)
class NewTrainerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "branch",
        "email",
        "phone_number",
        "members_count",
    ]
    search_fields = [
        "id",
        "username",
        "email",
    ]
    list_filter = [
        "branch",
        "email",
    ]


@admin.register(BranchTrainer)
class BranchTrainerAdmin(admin.ModelAdmin):
    list_display = [
        "trainer",
        "branch",
        "created_at",
    ]
    search_fields = [
        "id",
        "trainer",
        "subscriptions",
    ]
    list_filter = [
        "trainer",
        "subscriptions",
        "created_at",
    ]


@admin.register(BranchMember)
class BranchMemberAdmin(admin.ModelAdmin):
    list_display = [
        "trainee",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "id",
        "trainee",
    ]
    list_filter = [
        "trainee",
        "created_at",
    ]


@admin.register(MemberSubscription)
class MemberSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "member",
        "subscription_plan",
        "start_date",
        "end_date",
    ]
    search_fields = [
        "id",
        "member",
        "subscription",
    ]
    list_filter = [
        "member",
        "start_date",
    ]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "owner",
        "is_verified",
        "get_name",
        "slug",
        "address",
        "details",
        "total_members",
        "new_members",
        "is_open",
    ]
    search_fields = [
        "id",
        "name",
    ]
    list_filter = [
        "club__property_name",
        "created_at",
    ]
    readonly_fields = [
        "slug",
        "avg_ratings",
        "number_of_ratings",
        "total_members",
        "new_members",
    ]

    def get_name(self, obj):
        return obj.club.property_name

    get_name.short_description = "Branch Name"


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "date",
        "is_present",
    ]
    search_fields = [
        "id",
        "branch_member",
        "is_present",
    ]
    list_filter = [
        "branch_member",
        "date",
    ]


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "message",
        "branch",
        "created_at",
    ]
    search_fields = [
        "id",
        "branch",
    ]
    list_filter = [
        "branch",
        "created_at",
    ]


@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "day",
        "is_open",
        "branch",
    ]
    search_fields = [
        "id",
        "branch",
    ]
    list_filter = [
        "day",
        "branch",
    ]


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "from_time",
        "to_time",
        "day",
    ]
    search_fields = [
        "id",
        "day",
    ]
    list_filter = [
        "day",
    ]


@admin.register(Facilities)
class FacilitiesAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "icon",
        "branch",
    ]
    search_fields = [
        "id",
        "branch",
    ]
    list_filter = [
        "branch",
    ]


@admin.register(BranchGallery)
class BranchGalleryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "gallery",
        "branch",
    ]
    search_fields = [
        "id",
        "branch",
    ]
    list_filter = [
        "branch",
    ]
