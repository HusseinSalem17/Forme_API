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


class CustomUserClubPostSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
            "date_of_birth",
            "profile_picture",
            "gender",
            "location",
            "phone_number",
        ]
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
            "date_of_birth": {"required": False},
            "profile_picture": {"required": False},
            "gender": {"required": False},
            "location": {"required": False},
            "phone_number": {"required": True},
        }

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop(
            "confirm_password"
        )  # Remove confirm_password before creating user
        user = CustomUser.objects.create_user(**validated_data)
        return user


class CustomUserClubPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "date_of_birth",
            "profile_picture",
            "gender",
            "location",
            "phone_number",
        ]
        extra_kwargs = {
            "username": {"required": False},
            "date_of_birth": {"required": False},
            "profile_picture": {"required": False},
        }


class TraineeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Trainee
        fields = [
            "user",
            "fitness_goals",
            "current_physical_level",
        ]
