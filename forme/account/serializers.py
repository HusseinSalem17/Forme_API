from rest_framework import serializers

from .models import CustomUser, Owner, Rating, TraineeProfile, TrainerProfile
from rest_framework import serializers
from django.db.models import Avg


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "date_of_birth",
            "profile_picture",
            "location",
            "phone_number",
            "created_at",
            "updated_at",
        ]


class TraineeProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    trainers = CustomUserSerializer(many=True)

    class Meta:
        model = TraineeProfile
        fields = [
            "user",
            "gender",
            "fitness_goals",
            "current_fitness_level",
            "trainers",
        ]


class RatingSerializer(serializers.ModelSerializer):
    trainee = TraineeProfileSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = [
            "trainee",
            "rating",
            "comment",
            "created_at",
        ]


class TrainerProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    trainees = CustomUserSerializer(many=True)
    ratings = RatingSerializer(many=True)
    number_of_ratings = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = TrainerProfile
        fields = [
            "user",
            "gender",
            "slug",
            "bio",
            "specialization",
            "certification_files",
            "id_card",
            "background_image",
            "trainees",
            "experience",
            "verified",
            "number_of_trainees",
            "ratings",
            "number_of_ratings",
            "avg_rating",
        ]

    def get_number_of_ratings(self, obj):
        return obj.ratings.count()

    def get_avg_rating(self, obj):
        average_rating = obj.ratings.aggregate(Avg("rating"))["rating__avg"]
        return round(average_rating, 2) if average_rating is not None else 0


class OwnerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Owner
        fields = [
            "user",
        ]
