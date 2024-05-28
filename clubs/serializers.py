from authentication.models import CustomUser, Location
from authentication.serializers import (
    CustomUserClubAddSerializer,
    CustomUserUpdateSerializer,
    CustomUserSerializer,
    LocationSerializer,
)
from trainings.models import Program, Trainee, Trainer, Workout
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
    Document,
    Facilities,
    MemberSubscription,
    Subscription,
    SubscriptionPlan,
    Time,
    WorkingHours,
    NewTrainer,
)
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from django.db import transaction

from .utils import calculate_end_date

import base64
from django.core.files.base import ContentFile
from drf_extra_fields.fields import Base64ImageField


class DocumentAddSerializer(serializers.ModelSerializer):
    document = serializers.CharField()

    class Meta:
        model = Document
        fields = [
            "document",
        ]


class ClubAddSerializer(serializers.ModelSerializer):
    documents = DocumentAddSerializer(many=True, required=False)

    class Meta:
        model = Club
        fields = [
            "property_name",
            "club_website",
            "club_registration_number",
            "country",
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
            "sport_field": {
                "required": True,
            },
            "country": {
                "required": False,
            },
        }

    def create(self, validated_data):
        print("reached here Noww")
        club = Club.objects.create(**validated_data)
        club_content_type = ContentType.objects.get_for_model(club)
        documents_files = self.context["request"].FILES.getlist("club.documents")
        if documents_files:
            for doc_file in documents_files:
                print("doc_file", doc_file)
                Document.objects.create(club=club, document=doc_file)
        return club


class ClubUpdateSerializer(serializers.ModelSerializer):
    documents = DocumentAddSerializer(many=True)

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

    def update(self, instance, validated_data):
        documents_data = validated_data.pop("documents", [])
        instance.property_name = validated_data.get(
            "property_name", instance.property_name
        )
        instance.club_website = validated_data.get(
            "club_website", instance.club_website
        )
        instance.club_registration_number = validated_data.get(
            "club_registration_number", instance.club_registration_number
        )
        instance.sport_field = validated_data.get("sport_field", instance.sport_field)
        instance.save()
        for doc_data in documents_data:
            Document.objects.create(club=instance, **doc_data)
        return instance


class TrainerExistingAddSerializer(serializers.ModelSerializer):
    trainer_slug = serializers.CharField()

    class Meta:
        model = BranchTrainer
        fields = ["trainer_slug"]

    def validate_trainer_slug(self, value):
        if not Trainer.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Trainer not found")
        return value

    def create(self, validated_data):
        trainer_slug = validated_data.get("trainer_slug")
        trainer = Trainer.objects.get(slug=trainer_slug)
        branch = Branch.objects.filter(owner=self.context["request"].user).first()
        if BranchTrainer.objects.filter(trainer=trainer).exists():
            raise serializers.ValidationError({"trainer": "Trainer already exists"})
        branch_trainer = BranchTrainer.objects.create(trainer=trainer, branch=branch)
        return branch_trainer


class TrainerExistingUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchTrainer
        fields = ["subscriptions"]

    def update(self, instance, validated_data):
        subscription = validated_data.get("subscriptions")
        instance.subscription = subscription
        instance.save()
        return instance


class BranchAddSerializer(serializers.ModelSerializer):
    owner = CustomUserClubAddSerializer()
    club = ClubAddSerializer()

    class Meta:
        model = Branch
        fields = [
            "owner",
            "club",
            "address",
            "details",
        ]
        extra_kwargs = {
            "owner": {
                "required": True,
            },
            "club": {
                "required": True,
            },
            "address": {
                "required": True,
            },
            "details": {
                "required": True,
            },
        }

    def create(self, validated_data):
        owner_data = validated_data.pop("owner")
        club_data = validated_data.pop("club")

        owner_serializer = CustomUserClubAddSerializer(data=owner_data)
        club_serializer = ClubAddSerializer(
            data=club_data, context={"request": self.context["request"]}
        )

        if not owner_serializer.is_valid():
            raise serializers.ValidationError(owner_serializer.errors)
        if not club_serializer.is_valid():
            raise serializers.ValidationError(club_serializer.errors)

        with transaction.atomic():
            owner = owner_serializer.save()
            club = club_serializer.save()

            branch = Branch.objects.create(owner=owner, club=club, **validated_data)

        return branch


class BranchLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={"required": "Email address is required."},
    )
    password = serializers.CharField(
        required=True,
        error_messages={"required": "Password is required."},
    )

    def validate(self, data):
        # Ensure that 'email' and 'password' are provided
        email = data.get("email")
        password = data.get("password")
        user = CustomUser.objects.filter(email=email).first()
        branch = Branch.objects.filter(owner=user).first()
        if user is None:
            raise serializers.ValidationError({"email": "User does not exist."})
        if not email:
            raise serializers.ValidationError({"email": "Email is required."})
        if not password:
            raise serializers.ValidationError({"password": "Password is required."})
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Password is incorrect."})
        if not user.is_owner:
            raise serializers.ValidationError({"email": "User is not an owner."})
        if not branch:
            raise serializers.ValidationError({"email": "Branch does not exist."})
        if not branch.is_verified:
            raise serializers.ValidationError(
                {"verification": "Branch is not verified."}
            )
        return data


class BranchRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "owner",
            "details",
            "location",
        ]
        extra_kwargs = {
            "name": {
                "required": True,
            },
            "address": {
                "required": True,
            },
            "location": {
                "required": True,
            },
        }


class BranchGallerySerializer(serializers.ModelSerializer):
    gallery = serializers.ImageField()

    class Meta:
        model = BranchGallery
        fields = [
            "gallery",
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


class TimeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = [
            "from_time",
            "to_time",
        ]


class WorkingHoursUpdateSerializer(serializers.ModelSerializer):
    day_time = TimeUpdateSerializer(many=True)

    class Meta:
        model = WorkingHours
        fields = [
            "day",
            "is_open",
            "day_time",
        ]


class FacilitiesAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = [
            "name",
            "icon",
        ]


class BranchUpdateSerializer(serializers.ModelSerializer):
    owner = CustomUserUpdateSerializer()
    club = ClubUpdateSerializer()
    facilities = FacilitiesAddSerializer(many=True)
    working_hours = WorkingHoursSerializer(many=True)

    class Meta:
        model = Branch
        fields = [
            "owner",
            "club",
            "address",
            "details",
            "facilities",
            "working_hours",
        ]
        extra_kwargs = {
            "owner": {
                "required": False,
            },
            "club": {
                "required": False,
            },
            "address": {
                "required": False,
            },
            "details": {
                "required": False,
            },
            "facilities": {
                "required": False,
            },
            "working_hours": {
                "required": False,
            },
        }

    def update(self, instance, validated_data):
        owner_data = validated_data.pop("owner", None)
        club_data = validated_data.pop("club", None)
        facilities = validated_data.pop("facilities", None)
        working_hours = validated_data.pop("working_hours", None)

        with transaction.atomic():
            if owner_data is not None:
                owner_serializer = CustomUserUpdateSerializer(
                    instance.owner, data=owner_data, partial=True
                )
                if owner_serializer.is_valid(raise_exception=True):
                    owner_serializer.update(instance.owner, owner_data)

            if club_data is not None:
                club_serializer = ClubUpdateSerializer(
                    instance.club, data=club_data, partial=True
                )
                if club_serializer.is_valid(raise_exception=True):
                    club_serializer.update(instance.club, club_data)

            if facilities is not None:
                facility_ids = [facility.get("id") for facility in facilities]
                instance.facilities.clear()
                instance.facilities.add(*facility_ids)

            if working_hours is not None:
                for working_hour in working_hours:
                    day = working_hour.get("day")
                    time_data = working_hour.get("day_time")
                    working_hour_instance = WorkingHours.objects.get(day=day)
                    time_instance = Time.objects.filter(day=working_hour_instance)
                    for time in time_data:
                        time_instance.update(
                            from_time=time.get("from_time"), to_time=time.get("to_time")
                        )

            instance.address = validated_data.get("address", instance.address)
            instance.details = validated_data.get("details", instance.details)
            instance.save()

        return instance


class SubscriptionPlanAddSerializer(serializers.ModelSerializer):
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
            "id",
            "duration",
            "price",
            "is_offer",
            "max_members",
            "expiration_date",
            "is_added",
        ]


# class SubscriptionSerializer(serializers.ModelSerializer):
#     subscription_plans = serializers.SerializerMethodField()

#     class Meta:
#         model = Subscription
#         fields = [
#             "id",
#             "title",
#             "price",
#             "subscription_plans",
#             "current_members_count",
#             "created_at",
#             "updated_at",
#         ]

#     def get_subscription_plans(self, obj):
#         subscription_plan = SubscriptionPlan.objects.filter(subscription=obj)
#         return SubscriptionPlanSerializer(subscription_plan, many=True).data


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


class SubscriptionAddSerializer(serializers.ModelSerializer):
    subscription_plan = SubscriptionPlanAddSerializer(required=False, many=True)

    class Meta:
        model = Subscription
        fields = [
            "title",
            "min_age",
            "max_age",
            "price",
            "max_members",
            "target_gender",
            "subscription_plan",
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

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context["request"].user
            if not user.is_owner:
                raise serializers.ValidationError({"user": "User is not an owner."})
            subscription_plans_data = validated_data.pop("subscription_plan")
            subscription = Subscription.objects.create(**validated_data)
            if subscription_plans_data is not None:
                for subscription_plan in subscription_plans_data:
                    duration = subscription_plan.get("duration", None)
                    s = SubscriptionPlan.objects.get(
                        duration=duration, subscription=subscription
                    )
                    for key, value in subscription_plan.items():
                        setattr(s, key, value)

                    s.save()
            return subscription


class SubscriptionPlanUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionPlan
        fields = [
            "duration",
            "price",
            "is_offer",
            "max_members",
            "expiration_date",
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

    def update(self, instance, validated_data):
        instance.duration = validated_data.get("duration", instance.duration)
        instance.price = validated_data.get("price", instance.price)
        instance.is_offer = validated_data.get("is_offer", instance.is_offer)
        instance.max_members = validated_data.get("max_members", instance.max_members)
        instance.is_added = validated_data.get("is_added", True)
        instance.expiration_date = validated_data.get(
            "expiration_date", instance.expiration_date
        )
        instance.save()
        return instance


class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    subscription_plans = SubscriptionPlanUpdateSerializer(required=False, many=True)

    class Meta:
        model = Subscription
        fields = [
            "title",
            "min_age",
            "max_age",
            "subscription_plans",
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

    def update(self, instance, validated_data):
        with transaction.atomic():
            user = self.context["request"].user
            if not user.is_owner:
                raise serializers.ValidationError({"user": "User is not an owner."})
            if not instance.branch.owner == user:
                raise serializers.ValidationError(
                    {"owner": "User is not the owner of the branch."}
                )

            instance.title = validated_data.get("title", instance.title)
            instance.price = validated_data.get("price", instance.price)
            instance.min_age = validated_data.get("min_age", instance.min_age)
            instance.max_age = validated_data.get("max_age", instance.max_age)
            instance.max_members = validated_data.get(
                "max_members", instance.max_members
            )
            subscription_plans_data = validated_data.pop("subscription_plans", None)
            if subscription_plans_data is not None:
                for subscription_plan in subscription_plans_data:
                    duration = subscription_plan.get("duration", None)
                    s = SubscriptionPlan.objects.get(
                        duration=duration, subscription=instance
                    )
                    for key, value in subscription_plan.items():
                        setattr(s, key, value)

                s.save()
            instance.save()
            return instance


class SubscriptionSerializer(serializers.ModelSerializer):
    subscription_plan = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

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


class TraineeSubscriptionSerializer(serializers.ModelSerializer):
    trainers = serializers.SerializerMethodField()
    new_trainers = serializers.SerializerMethodField()
    subscription_plan = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Subscription
        fields = [
            "id",
            "title",
            "price",
            "trainers",
            "is_completed",
            "max_members",
            "subscription_plan",
            "created_at",
            "updated_at",
        ]

    def get_subscription_plan(self, obj):
        subscription_plan = SubscriptionPlan.objects.filter(subscription=obj)
        return SubscriptionPlanSerializer(subscription_plan, many=True).data

    def get_trainers(self, obj):
        trainers = BranchTrainer.objects.filter(subscription=obj)
        return TraineeBranchTrainerSerializer(trainers, many=True).data

    def get_new_trainers(self, obj):
        new_trainers = NewTrainer.objects.filter(subscription=obj)
        return TraineeNewTrainerSerializer(new_trainers, many=True).data


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "date",
            "is_present",
        ]


class MemberSubscriptionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberSubscription
        fields = [
            "trainer",
            "subscription_plan",
        ]
        extra_kwargs = {
            "trainer": {
                "required": True,
            },
            "subscription_plan": {
                "required": True,
            },
        }

    def validate_subscription_plan(self, value):
        if not value:
            raise serializers.ValidationError("Subscription plan is required.")
        return value


class MemberSubscriptionSerializer(serializers.ModelSerializer):
    # subscription = serializers.SerializerMethodField()

    class Meta:
        model = MemberSubscription
        fields = [
            "id",
            "trainer",
            # "subscriptions",
            "created_at",
            "updated_at",
        ]


class NewTrainerAddSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField(required=False)

    class Meta:
        model = NewTrainer
        fields = [
            "email",
            "username",
            "profile_picture",
            "phone_number",
            "subscriptions",
        ]
        extra_kwargs = {
            "email": {
                "required": True,
            },
            "username": {
                "required": True,
            },
            "phone_number": {
                "required": False,
            },
            "subscriptions": {"required": False},
        }

    def validate(self, data):
        # Ensure that 'email' and 'username' are provided
        if not data.get("email"):
            raise serializers.ValidationError("Email is required.")
        if not data.get("username"):
            raise serializers.ValidationError("Username is required.")
        return data


class NewTrainerUpdateSerializer(serializers.ModelSerializer):
    profile_picture = serializers.CharField(required=False)

    class Meta:
        model = NewTrainer
        fields = [
            "email",
            "username",
            "profile_picture",
            "phone_number",
            "subscriptions",
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
            },
            "subscriptions": {
                "required": False,
            },
        }

    def update(self, instance, validated_data):
        profile_picture = validated_data.pop("profile_picture", None)
        if profile_picture:
            format, imgstr = profile_picture.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=f"{instance.username}.{ext}"
            )
            instance.profile_picture = data
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.save()
        return instance


class NewTrainerSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSummarySerializer(many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = NewTrainer
        fields = [
            "id",
            "username",
            "subscriptions",
            "email",
            "profile_picture",
            "phone_number",
            "members_count",
            "created_at",
            "updated_at",
        ]

    def get_subscription(self, obj):
        subscription = Subscription.objects.filter(branch=obj)
        return SubscriptionSummarySerializer(subscription, many=True).data


class TraineeNewTrainerSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSummarySerializer(many=True)  # Add 'many=True' here
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = NewTrainer
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "profile_picture",
            "created_at",
            "updated_at",
        ]


class BranchTrainerSerializer(serializers.ModelSerializer):
    trainer = TrainerListSerializer()
    subscriptions = SubscriptionSummarySerializer(many=True)  # Add 'many=True' here
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = BranchTrainer
        fields = [
            "trainer",
            "subscriptions",
            "created_at",
            "updated_at",
        ]


class TraineeBranchTrainerSerializer(serializers.ModelSerializer):
    trainer = TrainerListSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = BranchTrainer
        fields = [
            "trainer",
            "created_at",
            "updated_at",
        ]


class SubscriptionUpdateSeralizer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Subscription
        fields = [
            "id",
            "title",
            "price",
            "max_members",
        ]
        extra_kwargs = {
            "title": {
                "required": False,
            },
            "price": {
                "required": False,
            },
            "max_members": {
                "required": False,
            },
        }


class BranchTrainerUpdateSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionUpdateSeralizer(many=True)

    class Meta:
        model = BranchTrainer
        fields = [
            "subscriptions",
        ]
        extra_kwargs = {
            "subscriptions": {
                "required": True,
            },
        }

    def validate_subscription(self, value):
        if not value:
            raise serializers.ValidationError("Subscription is required.")
        return value

    def update(self, instance, validated_data):
        subscriptions = validated_data.get("subscriptions")

        if subscriptions is not None:
            for subscription in subscriptions:
                print("reached here0")
                subscription_id = subscription.get("id", None)
                if subscription_id:
                    try:
                        print("reached here 2")
                        subscription = Subscription.objects.get(id=subscription_id)
                        serializer = SubscriptionUpdateSeralizer(
                            subscription, data=subscription, partial=True
                        )
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        print("reached here1")
                    except Subscription.DoesNotExist:
                        raise serializers.ValidationError(
                            {"subscription": "Subscription does not exist."}
                        )
                else:
                    raise serializers.ValidationError(
                        {"subscription": "Subscription id does not exist."}
                    )

        instance.save()
        return instance


class BranchMemberPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchMember
        fields = [
            "trainee",
        ]


class BranchMemberJoinSerializer(serializers.Serializer):
    subscription_plan = serializers.IntegerField(
        required=True,
        error_messages={"required": "Subscription plan is required."},
    )
    start_date = serializers.DateField(
        required=True,
        error_messages={"required": "Start date is required."},
    )
    trainer = serializers.IntegerField(
        required=True,
        error_messages={"required": "Trainer is required."},
    )

    def validate_subscription_plan(self, value):
        if not SubscriptionPlan.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                {"subscription_plan": "Subscription plan does not exist."}
            )
        return value

    def validate_trainer(self, value):
        if not Trainer.objects.filter(slug=value).exists():
            raise serializers.ValidationError({"trainer": "Trainer does not exist."})
        return value

    def create(self, validated_data):
        subscription_plan = validated_data.get("subscription_plan")
        start_date = validated_data.get("start_date")
        trainer = validated_data.get("trainer")
        subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan)
        subscription = Subscription.objects.get(id=subscription_plan.subscription.id)
        branch = Branch.objects.get(id=subscription.branch.id)
        branch.current_balance += subscription_plan.price
        branch.total_balance += subscription_plan.price
        branch.new_members += 1
        branch.total_members += 1
        trainee = Trainee.objects.get(user=self.context["request"].user)
        trainer = BranchTrainer.objects.get(id=trainer)
        if not trainee:
            raise serializers.ValidationError({"trainee": "Trainee does not exist."})
        if BranchMember.objects.filter(trainee=trainee).exists():
            raise serializers.ValidationError(
                {"BranchMember": "Branch Member is already exist"}
            )
        else:
            branch.total_members += 1
            branch.new_members += 1
            duration = subscription_plan.duration
            end_date = calculate_end_date(duration, start_date)
            branchMember = BranchMember.objects.create(trainee=trainee)
            MemberSubscription.objects.create(
                member=branchMember,
                trainer=trainer,
                subscription=subscription,
                subscription_plan=subscription_plan,
                start_date=start_date,
                end_date=end_date,
            )
            branch.members.add(branchMember)
            return branchMember


class BranchMemberUpdateSerializer(serializers.ModelSerializer):
    subscription_plan = serializers.IntegerField(
        required=False,
        error_messages={"required": "Subscription plan is required."},
    )
    trainer = serializers.IntegerField(
        required=False,
        error_messages={"required": "Trainer is required."},
    )

    class Meta:
        model = MemberSubscription
        fields = [
            "subscription_plan",
            "trainer",
        ]

    def validate_subscription_plan(self, value):
        if not Subscription.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                {"subscription_plan": "Subscription plan does not exist."}
            )
        return value

    def validate_trainer(self, value):
        if not BranchTrainer.objects.filter(id=value).exists():
            raise serializers.ValidationError({"trainer": "Trainer does not exist."})
        return value

    def update(self, instance, validated_data):
        print('reached here 12')
        subscription_plan = validated_data.get("subscription_plan")
        trainer = validated_data.get("trainer")
        if subscription_plan:
            subscription_plan = Subscription.objects.get(id=subscription_plan)
            trainer = BranchTrainer.objects.get(id=trainer)
            instance.subscription = subscription_plan
            instance.trainer = trainer
            instance.save()
        return instance


class BranchMemberSerializer(serializers.ModelSerializer):
    # trainee = TraineeSerializer()
    member_subscription = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()

    class Meta:
        model = BranchMember
        fields = [
            # "trainee",
            "member_subscription",
            "attendance",
            "created_at",
            "updated_at",
        ]

    def get_member_subscription(self, obj):
        member_subscription = MemberSubscription.objects.filter(member=obj)
        if not member_subscription.exists():
            return None
        # Explicitly convert queryset to list (should not be necessary but can be tried if issues persist)
        return MemberSubscriptionSerializer(list(member_subscription), many=True).data

    def get_attendance(self, obj):
        attendance = Attendance.objects.filter(branch_member=obj)
        if not attendance:
            return None
        return AttendancesSerializer(attendance, many=True).data


class AttendanceSerializerTemp(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["date", "is_present"]

class SubscriptionPlanMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "duration",
            "price",
            "is_offer",
        ]
        
class MemberSubscriptionSerializerTemp(serializers.ModelSerializer):
    attendance = AttendanceSerializerTemp(many=True, read_only=True)
    subscription_plan = SubscriptionPlanMemberSerializer()
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = MemberSubscription
        fields = [
            "id",
            "trainer",
            "subscription_plan",
            "subscription",
            "state",
            "start_date",
            "end_date",
            "attendance",
        ]

    def get_subscription(self, obj):
        subscription = Subscription.objects.get(id=obj.subscription.id)
        return SubscriptionSummarySerializer(subscription).data


class ClubTraineeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Trainee
        fields = [
            "user",
            "fitness_goals",
            "current_physical_level",
        ]


class BranchMemberSerializerTemp(serializers.ModelSerializer):
    trainee = ClubTraineeSerializer()
    member_subscription = MemberSubscriptionSerializerTemp(many=True)

    class Meta:
        model = BranchMember
        fields = [
            "id",
            "trainee",
            "member_subscription",
            "created_at",
            "updated_at",
        ]


class BranchMemberPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchMember
        fields = [
            "trainee",
            "duration",
            "amount",
            "trainer",
            "subscriptions",
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


class AttendancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "is_present",
        ]


class ClubDetailSerializer(serializers.ModelSerializer):
    # branches = serializers.SerializerMethodField()
    # documents = DocumentSerializer(many=True)

    class Meta:
        model = Club
        fields = [
            "id",
            "property_name",
            "club_website",
            "club_registration_number",
            "country",
            # "documents",
            "sport_field",
            # "branches",
            "created_at",
            "updated_at",
        ]

    # def get_documents(self, obj):
    #     documents = Document.objects.filter(club=obj)
    #     return DocumentSerializer(documents, many=True).data

    # def get_branches(self, obj):
    #     branches = Branch.objects.filter(club=obj)
    #     return BranchListSerializer(branches, many=True).data


class BranchDetailSerializer(serializers.ModelSerializer):
    trainers = serializers.SerializerMethodField()
    owner = CustomUserSerializer()
    location = serializers.SerializerMethodField()
    new_trainers = serializers.SerializerMethodField()
    club = ClubDetailSerializer()
    members = serializers.SerializerMethodField()
    working_hours = serializers.SerializerMethodField()
    subscriptions = serializers.SerializerMethodField()
    facilities = serializers.SerializerMethodField()
    reviews = ReviewsDetailSerializer(many=True)
    galleries = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Branch
        fields = [
            "id",
            "club",
            "owner",
            "slug",
            "address",
            "location",
            "working_hours",
            "details",
            "trainers",
            "new_trainers",
            "members",
            "subscriptions",
            "total_members",
            "new_members",
            "is_open",
            "current_balance",
            "total_balance",
            "facilities",
            "reviews",
            "galleries",
            "created_at",
            "updated_at",
        ]

    def get_trainers(self, obj):
        trainers = BranchTrainer.objects.filter(branch=obj)
        return BranchTrainerSerializer(trainers, many=True).data

    def get_new_trainers(self, obj):
        new_trainers = NewTrainer.objects.filter(branch=obj)
        return NewTrainerSerializer(new_trainers, many=True).data

    def get_working_hours(self, obj):
        working_hours = WorkingHours.objects.filter(branch=obj)
        return WorkingHoursSerializer(working_hours, many=True).data

    def get_subscriptions(self, obj):
        subscriptions = Subscription.objects.filter(branch=obj)
        return SubscriptionSerializer(subscriptions, many=True).data

    def get_members(self, obj):
        members = BranchMember.objects.filter(branch=obj)
        return BranchMemberSerializerTemp(members, many=True).data

    def get_facilities(self, obj):
        facilities = Facilities.objects.filter(branch=obj)
        return FacilitiesSerializer(facilities, many=True).data

    def get_location(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        location = Location.objects.get(content_type=content_type, object_id=obj.id)
        return LocationSerializer(location).data

    def get_galleries(self, obj):
        galleries = BranchGallery.objects.filter(branch=obj)
        return BranchGallerySerializer(galleries, many=True).data


class TraineeBranchDetailSerializer(serializers.ModelSerializer):
    trainers = serializers.SerializerMethodField()
    owner = CustomUserSerializer()
    location = serializers.SerializerMethodField()
    new_trainers = serializers.SerializerMethodField()
    subscriptions = serializers.SerializerMethodField()
    facilities = serializers.SerializerMethodField()
    reviews = ReviewsDetailSerializer(many=True)
    galleries = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Branch
        fields = [
            "id",
            "owner",
            "slug",
            "address",
            "location",
            "details",
            "trainers",
            "new_trainers",
            "subscriptions",
            "total_members",
            "new_members",
            "is_open",
            "facilities",
            "reviews",
            "galleries",
            "created_at",
            "updated_at",
        ]

    def get_trainers(self, obj):
        trainers = BranchTrainer.objects.filter(branch=obj)
        return TraineeBranchTrainerSerializer(trainers, many=True).data

    def get_new_trainers(self, obj):
        new_trainers = NewTrainer.objects.filter(branch=obj)
        return TraineeNewTrainerSerializer(new_trainers, many=True).data

    def get_subscriptions(self, obj):
        subscriptions = Subscription.objects.filter(branch=obj)
        return SubscriptionSerializer(subscriptions, many=True).data

    def get_facilities(self, obj):
        facilities = Facilities.objects.filter(branch=obj)
        return FacilitiesSerializer(facilities, many=True).data

    def get_location(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        location = Location.objects.get(content_type=content_type, object_id=obj.id)
        return LocationSerializer(location).data

    def get_galleries(self, obj):
        galleries = BranchGallery.objects.filter(branch=obj)
        return BranchGallerySerializer(galleries, many=True).data


class NewTrainerConvertSerializer(serializers.Serializer):
    trainer_slug = serializers.CharField(
        required=True,
        error_messages={"required": "Trainer slug is required."},
    )

    def validate_trainer_slug(self, value):
        if not Trainer.objects.filter(slug=value).exists():
            raise serializers.ValidationError({"trainer": "Trainer does not exist."})
        return value

    def create(self, validated_data):
        id = self.context["new_trainer_id"]
        trainer_slug = validated_data.get("trainer_slug")
        new_trainer = NewTrainer.objects.get(id=id)
        if new_trainer is None:
            raise serializers.ValidationError(
                {"new_trainer": "New trainer does not exist."}
            )
        trainer = Trainer.objects.get(slug=trainer_slug)
        if trainer is None:
            raise serializers.ValidationError({"trainer": "Trainer does not exist."})
        if BranchTrainer.objects.filter(trainer=trainer).exists():
            raise serializers.ValidationError({"trainer": "Trainer already exists."})

        branch_trainer = BranchTrainer.objects.create(
            trainer=trainer,
            members_count=new_trainer.members_count,
        )
        branch_trainer.subscriptions.set(new_trainer.subscriptions.all())
        new_trainer.delete()
        return branch_trainer


class BranchListSerializer(serializers.ModelSerializer):
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = [
            "id",
            "slug",
            "details",
            "address",
            "is_open",
            "subscriptions",
        ]

    def get_subscriptions(self, obj):
        subscriptions = Subscription.objects.filter(branch=obj)
        return SubscriptionSummarySerializer(subscriptions, many=True).data


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


class ClubsListSerializer(serializers.ModelSerializer):
    branches = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = [
            "id",
            "property_name",
            "club_website",
            "club_registration_number",
            "country",
            # "documents",
            "sport_field",
            "branches",
            "created_at",
            "updated_at",
        ]

    def get_branches(self, obj):
        branches = Branch.objects.filter(club=obj)
        return BranchListSerializer(branches, many=True).data


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "is_present",
        ]

    def update(self, instance, validated_data):
        instance.is_present = validated_data.get("is_present", instance.is_present)
        instance.save()
        return instance


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
class SearchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        fields = ["id", "type", "name"]

    def get_type(self, obj):
        if isinstance(obj, Workout):
            return "Workout"
        elif isinstance(obj, Program):
            return "Program"
        elif isinstance(obj, Trainer):
            return "Trainer"
        elif isinstance(obj, Club):
            return "Club"
        else:
            return "Unknown"

    def get_name(self, obj):
        if isinstance(obj, Workout):
            return obj.workout_name
        elif isinstance(obj, Program):
            return obj.program_name
        elif isinstance(obj, Trainer):
            return obj.trainer_name
        elif isinstance(obj, Club):
            return obj.club_name
        else:
            return ""
