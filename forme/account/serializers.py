from rest_framework import serializers


from .models import CustomUser, Trainee


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
            "gender",
            "phone_number",
            "created_at",
            "updated_at",
        ]


class TraineeProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Trainee
        fields = [
            "user",
            "fitness_goals",
            "current_physical_level",
        ]
