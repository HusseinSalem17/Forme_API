from account.serializers import CustomUserSerializer, TraineeSerializer
from trainings.serializers import (
    TrainerListSerializer,
    ReviewsDetailSerializer,
)
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
from rest_framework import serializers


class BranchGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchGallery
        fields = [
            "galleries",
        ]


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = [
            "id",
            "name",
            "icon",
        ]


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = [
            "id",
            "from_time",
            "to_time",
        ]


class WorkingHoursSerializer(serializers.ModelSerializer):
    day_time = serializers.SerializerMethodField()

    class Meta:
        model = WorkingHours
        fields = [
            "id",
            "day",
            "is_open",
            "day_time",
        ]

    def get_day_time(self, obj):
        time = Time.objects.filter(day=obj)
        return TimeSerializer(time, many=True).data


class SubscriptionPlanPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            "duration",
            "price",
            "is_offer",
            "max_members",
            "expiration_date",
            "is_added",
        ]
        extra_kwargs = {
            "duration": {
                "required": False,
            },
            "price": {
                "required": False,
            },
            "is_offer": {
                "required": False,
            },
            "max_members": {
                "required": False,
            },
            "expiration_date": {
                "required": False,
            },
        }


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            "duration",
            "price",
            "is_offer",
            "max_members",
            "expiration_date",
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    subscription_plan = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = [
            "id",
            "title",
            "price",
            "subscription_plans",
            "current_members_count",
            "created_at",
            "updated_at",
        ]

    def get_subscription_plan(self, obj):
        subscription_plan = SubscriptionPlan.objects.filter(subscription=obj)
        return SubscriptionPlanSerializer(subscription_plan, many=True).data


class SubscriptionSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = [
            "id",
            "title",
            "price",
            "created_at",
            "updated_at",
        ]


class SubscriptionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = [
            "title",
            "min_age",
            "max_age",
            "price",
            "max_members",
            "target_gender",
        ]
        extra_kwargs = {
            "title": {
                "required": True,
            },
            "price": {
                "required": True,
            },
            "min_age": {
                "required": False,
            },
            "max_age": {
                "required": False,
            },
            "max_members": {
                "required": False,
            },
            "target_gender": {
                "required": False,
            },
        }


class SubscriptionPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = [
            "title",
            "min_age",
            "max_age",
            "price",
            "max_members",
            "target_gender",
        ]
        extra_kwargs = {
            "title": {
                "required": False,
            },
            "price": {
                "required": False,
            },
            "min_age": {
                "required": False,
            },
            "max_age": {
                "required": False,
            },
            "max_members": {
                "required": False,
            },
            "target_gender": {
                "required": False,
            },
        }


class SubscriptionSerializer(serializers.ModelSerializer):
    subscription_plan = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = [
            "id",
            "title",
            "price",
            "is_completed",
            "max_members",
            "subscription_plan",
            "created_at",
            "updated_at",
        ]

    def get_subscription_plan(self, obj):
        subscription_plan = SubscriptionPlan.objects.filter(subscription=obj)
        return SubscriptionPlanSerializer(subscription_plan, many=True).data


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "date",
            "is_present",
        ]


class MemberSubscriptionSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSummarySerializer()
    subscription_plan = SubscriptionPlanSerializer()

    class Meta:
        model = MemberSubscription
        fields = [
            "id",
            "trainer",
            "subscription",
            "subscription_plan",
            "created_at",
            "updated_at",
        ]


class NewTrainerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewTrainer
        fields = [
            "email",
            "username",
            "phone_number",
            "subscription",
        ]
        extra_kwargs = {
            "email": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "username": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "phone_number": {
                "required": False,
                "allow_blank": True,
                "allow_null": True,
            },
            "subscription": {"required": False},
        }

    def validate(self, data):
        # Ensure that 'email' and 'username' are provided
        if not data.get("email"):
            raise serializers.ValidationError("Email is required.")
        if not data.get("username"):
            raise serializers.ValidationError("Username is required.")

        return data


class NewTrainerPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewTrainer
        fields = [
            "email",
            "username",
            "phone_number",
            "subscription",
        ]
        extra_kwargs = {
            "email": {
                "required": False,
            },
            "username": {
                "required": False,
            },
            "phone_number": {
                "required": False,
                "allow_blank": True,
                "allow_null": True,
            },
            "subscription": {
                "required": False,
            },
        }


class NewTrainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewTrainer
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "created_at",
            "updated_at",
        ]


class BranchTrainerSerializer(serializers.ModelSerializer):
    trainer = TrainerListSerializer()
    subscription = SubscriptionSummarySerializer(many=True)  # Add 'many=True' here

    class Meta:
        model = BranchTrainer
        fields = [
            "id",
            "trainer",
            "subscription",
            "created_at",
            "updated_at",
        ]


class BranchTrainerPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchTrainer
        fields = [
            "subscription",
        ]
        extra_kwargs = {
            "subscription": {
                "required": True,
            },
        }

    def validate_subscription(self, value):
        if not value:
            raise serializers.ValidationError("Subscription is required.")
        return value


class BranchMemberSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer()
    member_subscription = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()

    class Meta:
        model = BranchMember
        fields = [
            "id",
            "trainee",
            "member_subscription",
            "attendance",
            "created_at",
            "updated_at",
        ]

    def get_member_subscription(self, obj):
        member_subscription = MemberSubscription.objects.filter(member=obj)
        return MemberSubscriptionSerializer(member_subscription, many=True).data

    def get_attendance(self, obj):
        attendance = Attendance.objects.filter(branch_member=obj)
        return AttendancesSerializer(attendance, many=True).data


class BranchMemberPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchMember
        fields = [
            "trainee",
            "duration",
            "amount",
            "trainer",
            "subscription",
        ]


class BranchPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = [
            "address",
            "details",
        ]
        extra_kwargs = {
            "address": {
                "required": True,
            },
            "details": {
                "required": False,
            },
        }


class BranchPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = [
            "address",
            "details",
        ]
        extra_kwargs = {
            "address": {
                "required": False,
            },
            "details": {
                "required": False,
            },
        }


class BranchDetailSerializer(serializers.ModelSerializer):
    trainers = BranchTrainerSerializer(many=True)
    new_trainers = serializers.SerializerMethodField()
    members = BranchMemberSerializer(many=True)
    working_hours = serializers.SerializerMethodField()
    subscriptions = serializers.SerializerMethodField()
    branch_facilities = serializers.SerializerMethodField()
    branch_gallery = serializers.SerializerMethodField()
    reviews = ReviewsDetailSerializer(many=True)

    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "slug",
            "address",
            "working_hours",
            "details",
            "trainers",
            "new_trainers",
            "members",
            "subscriptions",
            "total_members",
            "new_members",
            "is_open",
            "branch_facilities",
            "branch_gallery",
            "reviews",
            "created_at",
            "updated_at",
        ]

    def get_new_trainers(self, obj):
        new_trainers = NewTrainer.objects.filter(branch=obj)
        return NewTrainerSerializer(new_trainers, many=True).data

    def get_working_hours(self, obj):
        working_hours = WorkingHours.objects.filter(branch=obj)
        return WorkingHoursSerializer(working_hours, many=True).data

    def get_subscriptions(self, obj):
        subscriptions = Subscription.objects.filter(branch=obj)
        return SubscriptionSerializer(subscriptions, many=True).data

    def get_branch_facilities(self, obj):
        facilities = Facilities.objects.filter(branch=obj)
        return FacilitiesSerializer(facilities, many=True).data

    def get_branch_gallery(self, obj):
        galleries = BranchGallery.objects.filter(branch=obj)
        return BranchGallerySerializer(galleries, many=True).data


class BranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "slug",
            "details",
            "location",
            "is_open",
        ]


class ContactUsSerializer(serializers.ModelSerializer):
    branch = BranchListSerializer()
    email = serializers.SerializerMethodField()

    class Meta:
        model = ContactUs
        fields = [
            "id",
            "email",
            "branch",
            "message",
            "created_at",
        ]

    def get_email(self, obj):
        branch = obj.branch
        return branch.owner.email


class AttendancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "is_present",
        ]


class ClubPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            "property_name",
            "club_website",
            "club_registration_number",
            "documents",
            "sport_field",
        ]
        extra_kwargs = {
            "property_name": {
                "required": True,
            },
            "club_website": {
                "required": False,
            },
            "club_registration_number": {
                "required": False,
            },
            "documents": {
                "required": False,
            },
            "sport_field": {
                "required": True,
            },
        }
class ClubPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            "property_name",
            "club_website",
            "club_registration_number",
            "documents",
            "sport_field",
        ]
        extra_kwargs = {
            "property_name": {
                "required": False,
            },
            "club_website": {
                "required": False,
            },
            "club_registration_number": {
                "required": False,
            },
            "documents": {
                "required": False,
            },
            "sport_field": {
                "required": False,
            },
        }


class ClubDetailSerializer(serializers.ModelSerializer):
    branches = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = [
            "id",
            "property_name",
            "club_website",
            "club_registration_number",
            "documents",
            "sport_field",
            "branches",
            "created_at",
            "updated_at",
        ]

    def get_branches(self, obj):
        branches = Branch.objects.filter(club=obj)
        return BranchListSerializer(branches, many=True).data


class ClubsListSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = [
            "id",
            "property_name",
            "club_website",
            "club_registration_number",
            "documents",
            "sport_field",
            "branch",
            "created_at",
            "updated_at",
        ]

    def get_branch(self, obj):
        branch = Branch.objects.filter(club=obj).first()
        return BranchListSerializer(branch).data if branch else None


# class OwnerDetailSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer()
#     branch = serializers.SerializerMethodField()

#     class Meta:
#         model = Owner
#         fields = [
#             "user",
#             "branch",
#         ]

#     def get_branch(self, obj):
#         branch = Branch.objects.filter(owner=obj)
#         return BranchDetailSerializer(branch, many=True).data


# class OwnerListSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer()
#     branch = serializers.SerializerMethodField()

#     class Meta:
#         model = Owner
#         fields = [
#             "user",
#             "branch",
#         ]

#     def get_branch(self, obj):
#         branch = Branch.objects.filter(owner=obj)
#         return BranchDetailSerializer(branch, many=True).data
