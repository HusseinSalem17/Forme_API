from account.serializers import CustomUserSerializer
from .models import Branch, Club, ClubGallery, Facilities, Owner, Plan
from rest_framework import serializers


class ClubGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubGallery
        fields = [
            "galleries",
            "description",
        ]


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "description",
            "price",
            "offer_price",
            "duration_in_months",
            "max_trainees_count",
            "current_trainees_count",
        ]


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = [
            "name",
            "icon",
        ]


class BranchDetailSerializer(serializers.ModelSerializer):
    branch_plans = serializers.SerializerMethodField()
    branch_facilities = serializers.SerializerMethodField()
    branch_gallery = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "slug",
            "details",
            "working_hours",
            "location",
            "is_open",
            "branch_plans",
            "branch_facilities",
            "branch_gallery",
        ]

    def get_branch_plans(self, obj):
        plans = Plan.objects.filter(branch=obj)
        return PlanSerializer(plans, many=True).data

    def get_branch_facilities(self, obj):
        facilities = Facilities.objects.filter(branch=obj)
        return FacilitiesSerializer(facilities, many=True).data

    def get_branch_gallery(self, obj):
        galleries = ClubGallery.objects.filter(branch=obj)
        return ClubGallerySerializer(galleries, many=True).data


class BranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "slug",
            "details",
            "working_hours",
            "location",
            "is_open",
        ]


class ClubDetailSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = [
            "id",
            "name",
            "branch",
            "created_at",
            "updated_at",
        ]

    def get_branch(self, obj):
        branch = Branch.objects.filter(club=obj)
        return BranchListSerializer(branch, many=True).data


class ClubsListSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = [
            "id",
            "name",
            "branch"
            "created_at",
            "updated_at",
        ]

    def get_branch(self, obj):
        branch = Branch.objects.filter(club=obj).first()
        return BranchListSerializer(branch).data if branch else None


class ClubDetailSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = [
            "id",
            "name",
            "branch",
            "created_at",
            "updated_at",
        ]

    def get_branch(self, obj):
        branch = Branch.objects.filter(club=obj)
        return BranchListSerializer(branch, many=True).data


class OwnerDetailSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    club = serializers.SerializerMethodField()

    class Meta:
        model = Owner
        fields = [
            "user",
            "club",
        ]

    def get_club(self, obj):
        club = Club.objects.filter(owner=obj)
        return ClubDetailSerializer(club, many=True).data


class OwnerListSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    club = serializers.SerializerMethodField()

    class Meta:
        model = Owner
        fields = [
            "user",
            "club",
        ]

    def get_club(self, obj):
        club = Club.objects.filter(owner=obj)
        return ClubsListSerializer(club, many=True).data
