from rest_framework import serializers

from .models import TraineeProfile


class TraineeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraineeProfile
        fields = "__all__"
        read_only_fields = ("user",)


class TraineeProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraineeProfile
        fields = [
            "id",
            "user__username",
            "user__email",
            "user__profile_picture",
            "user__location",
            "user__phone_number",
            "user__data_of_birth",
            "gender" "fitness_goal",
            "current_fitness_level",
            "trainers",
            "user__created_at",
            "user__updated_at",
        ]

