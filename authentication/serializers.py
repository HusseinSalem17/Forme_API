from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .threads import Util
from trainings.models import Document, Trainee, Trainer

from .models import OTP, CustomUser, Location

from drf_extra_fields.fields import Base64ImageField
import base64
from django.core.files.base import ContentFile


# For Register Screen
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={"required": "Email address is required."},
    )
    password = serializers.CharField(
        required=True,
        error_messages={"required": "Password is required."},
    )
    user_type = serializers.ChoiceField(
        choices=[("trainer", "Trainer"), ("trainee", "Trainee")],
        required=True,
        error_messages={"required": "User type is required."},
    )

    def validate(self, attrs):
        email = attrs.get("email", None)
        user_type = attrs.get("user_type", None)
        if not Util.check_otp_verified(email) or not Util.check_otp_validality(email):
            raise serializers.ValidationError("OTP is not verified or expired")
        if CustomUser.objects.filter(email=email).exists():
            print("reached hereeee Now")
            if CustomUser.objects.get(email=email).check_group(user_type + "s"):
                raise serializers.ValidationError(
                    f"Email is already in use for this {user_type}"
                )

        return attrs

    def create(self, validated_data):
        email = validated_data.pop("email", None)
        password = validated_data.pop("password", None)
        user_type = validated_data.pop("user_type", None)
        if user_type == "trainer":
            print("reached here now")
            if CustomUser.objects.filter(email=email).exists():
                if not CustomUser.objects.get(email=email).check_group("trainer"):
                    print("reached now")
                    print("reached")
                    user = CustomUser.objects.get(email=email)
                    user.join_group("trainers")
                    Trainer.objects.create(user=user).save()
                else:
                    raise serializers.ValidationError(
                        {"email": "Email is already in use for this trainer"}
                    )
            else:
                user = CustomUser.objects.create_trainer(
                    email,
                    password,
                )
                Trainer.objects.create(user=user).save()
            return user
        elif user_type == "trainee":
            if CustomUser.objects.filter(email=email).exists():
                if not CustomUser.objects.get(email=email).check_group("trainee"):
                    user = CustomUser.objects.get(email=email)
                    user.join_group("trainees")
                    Trainee.objects.create(user=user).save()
                else:
                    raise serializers.ValidationError(
                        {"email": "Email is already in use for this trainee"}
                    )
            else:
                user = CustomUser.objects.create_trainee(
                    email,
                    password,
                )
                Trainee.objects.create(user=user).save()
            return user
        else:
            raise serializers.ValidationError("Invalid user type")


# To request otp (for Register Screen)
class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={"required": "Email address is required."},
    )
    user_type = serializers.ChoiceField(
        choices=[("trainer", "Trainer"), ("trainee", "Trainee")],
        required=True,
        error_messages={"required": "User type is required."},
    )

    def validate(self, attrs):
        email = attrs.get("email", None)
        user_type = attrs.get("user_type", None)
        if user_type not in ["trainer", "trainee"]:
            raise serializers.ValidationError("Invalid user type")
        if CustomUser.objects.filter(email=email).exists() and CustomUser.objects.get(
            email=email
        ).check_group(
            user_type,
        ):
            raise serializers.ValidationError(
                f"Email is already in use for this {user_type}"
            )

        return attrs


# For Login Screen
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={"required": "Email address is required."},
    )
    password = serializers.CharField(
        required=True,
        error_messages={"required": "Password is required."},
    )
    user_type = serializers.ChoiceField(
        choices=[("trainer", "Trainer"), ("trainee", "Trainee")],
        required=True,
        error_messages={"required": "User type is required."},
    )

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        user_type = attrs.get("user_type", None)
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("User does not exist.")
        if not user.check_group(user_type):
            raise serializers.ValidationError("Invalid user type")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")
        return attrs


# To Set new password (for Forogt Password)
class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={"required": "Email address is required."},
    )
    new_password = serializers.CharField(
        required=True,
        error_messages={"required": "New Password is required."},
    )

    def check_otp(self, email):
        if not Util.check_otp_validality(email):
            raise serializers.ValidationError("OTP is expired")
        if not Util.check_otp_verified(email):
            raise serializers.ValidationError("OTP is invalid")

    def validate(self, attrs):
        email = attrs.get("email", None)
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("User not found")
        self.check_otp(email)
        return attrs


# To Forget Password Screen
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={"required": "Email address is required."},
    )

    def validate(self, attrs):
        email = attrs.get("email", None)
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("User not found")
        return attrs


# To Verify OTP Screen
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={"required": "Email address is required."},
    )
    otp = serializers.CharField(
        required=True,
        error_messages={"required": "OTP is required."},
    )

    def check_otp(self, email):
        if not Util.check_otp_validality(email):
            raise serializers.ValidationError("OTP is expired")
        if Util.check_otp_verified(email):
            raise serializers.ValidationError("OTP is invalid")

    def validate(self, attrs):
        email = attrs.get("email", None)
        otp = attrs.get("otp", None)
        otp_obj = OTP.objects.filter(email=email, otp=otp).first()
        if otp_obj is None:
            raise serializers.ValidationError("Invalid OTP")
        self.check_otp(email)
        return attrs


# To Reset Password Screen
class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        error_messages={"required": "old_password is required."},
    )
    new_password = serializers.CharField(
        required=True,
        error_messages={"required": "new_password is required."},
    )

    def validate(self, attrs):
        new_password = attrs.get("new_password", None)
        old_password = attrs.get("old_password", None)
        user = self.context.get("request").user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect")
        return attrs


# To Logout
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError("Token is expired or invalid")


# To Location
class LocationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Location
        fields = [
            "longitude",
            "latitude",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "longitude": {"required": True},
            "latitude": {"required": True},
            "created_at": {"required": False},
            "updated_at": {"required": False},
        }

    def validate(self, attrs):
        longitude = attrs.get("longitude", None)
        latitude = attrs.get("latitude", None)
        if not longitude:
            raise serializers.ValidationError("Longitude is required")
        if not latitude:
            raise serializers.ValidationError("Latitude is required")
        return attrs

    def create(self, validated_data):
        longitude = validated_data.pop("longitude", None)
        latitude = validated_data.pop("latitude", None)
        location = Location.objects.create(
            longitude=longitude, latitude=latitude, **validated_data
        )
        print("reached here create")
        return location

    def update(self, instance, validated_data):
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        print("reach here update")
        instance.save()
        return instance


class UploadProfilePictureSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()

    def validate(self, attrs):
        profile_picture = attrs.get("profile_picture", None)
        if not profile_picture:
            raise serializers.ValidationError("Profile picture is required")
        return attrs


class CompleteProfileUserSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField(required=False)
    gender = serializers.ChoiceField(
        choices=[("male", "Male"), ("female", "Female")],
        required=True,
        error_messages={"required": "gender is required."},
    )

    def validate_gender(self, value):
        if value not in dict(self.fields["gender"].choices):
            raise serializers.ValidationError("Invalid choice for gender.")
        return value

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "date_of_birth",
            "phone_number",
            "gender",
            "profile_picture",
            "country",
        ]
        extra_kwargs = {
            "username": {"required": True},
            "date_of_birth": {"required": True},
            "phone_number": {"required": False},
            "gender": {"required": True},
            "profile_picture": {"required": False},
            "country": {"required": True},
        }


# for complete profile trainer
class CompleteProfileTrainerSerializer(serializers.ModelSerializer):
    user = CompleteProfileUserSerializer()

    class Meta:
        model = Trainer
        fields = [
            "user",
            "sport_field",
        ]
        extra_kwargs = {
            "user": {"required": True},
            "sport_field": {"required": True},
        }

    def validate(self, attrs):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if not user.is_trainer():
            raise serializers.ValidationError("User is not a trainer")
        sport_field = attrs.get("sport_field", "")
        if user.is_trainer() and not sport_field:
            raise serializers.ValidationError("Sport field is required for trainers")
        return attrs

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        print("user_data birthdate", user_data)
        sport_field = validated_data.pop("sport_field", "")
        user = CustomUser.objects.get(id=instance.user.id)
        user_serializer = CompleteProfileUserSerializer(
            user, data=user_data, partial=True
        )
        if user_serializer.is_valid():
            user_serializer.save()
        trainer = Trainer.objects.get(user=user)
        trainer.sport_field = sport_field
        trainer.save()
        return trainer


# for update preference trainee and trainer
class UpdatePreferenceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "date_of_birth",
        ]
        extra_kwargs = {
            "date_of_birth": {"required": True},
        }

    def update(self, instance, validated_data):
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth
        )
        instance.save()
        return instance


# for update preference trainee
class UpdatePreferenceTraineeSerializer(serializers.ModelSerializer):
    user = UpdatePreferenceUserSerializer()

    class Meta:
        model = Trainee
        fields = [
            "user",
            "height",
            "weight",
            "fitness_goals",
            "current_physical_level",
        ]
        extra_kwargs = {
            "user": {"required": True},
            "height": {"required": True},
            "weight": {"required": True},
            "fitness_goals": {"required": True},
            "current_physical_level": {"required": True},
        }

    def update(self, instance, validated_data):
        instance.height = validated_data.get("height", instance.height)
        instance.weight = validated_data.get("weight", instance.weight)
        instance.fitness_goals = validated_data.get(
            "fitness_goals", instance.fitness_goals
        )
        instance.current_physical_level = validated_data.get(
            "current_physical_level", instance.current_physical_level
        )
        instance.save()

        return instance


class DocumentTrainerSerializer(serializers.ModelSerializer):
    document = serializers.CharField()

    class Meta:
        model = Document
        fields = [
            "document",
        ]


# for update preference trainer
class UpdatePreferenceTrainerSerializer(serializers.ModelSerializer):
    documents = DocumentTrainerSerializer(many=True, required=False)
    id_card = Base64ImageField(required=False)

    class Meta:
        model = Trainer
        fields = [
            "bio",
            "exp_injuries",
            "physical_disabilities",
            "languages",
            "id_card",
            "documents",
            "facebook_url",
            "instagram_url",
            "youtube_url",
        ]
        extra_kwargs = {
            "bio": {"required": False},
            "exp_injuries": {"required": True},
            "physical_disabilities": {"required": True},
            "id_card": {"required": False},
            "languages": {"required": False},
            "facebook_url": {"required": False},
            "instagram_url": {"required": False},
            "youtube_url": {"required": False},
        }

    def update(self, instance, validated_data):
        instance.bio = validated_data.get("bio", instance.bio)
        instance.exp_injuries = validated_data.get(
            "exp_injuries", instance.exp_injuries
        )
        instance.physical_disabilities = validated_data.get(
            "physical_disabilities", instance.physical_disabilities
        )
        instance.languages = validated_data.get("languages", instance.languages)
        instance.id_card = validated_data.get("id_card", instance.id_card)
        instance.facebook_url = validated_data.get(
            "facebook_url", instance.facebook_url
        )
        instance.instagram_url = validated_data.get(
            "instagram_url", instance.instagram_url
        )
        instance.youtube_url = validated_data.get("youtube_url", instance.youtube_url)

        documents_files = self.context["request"].FILES.getlist("documents")
        if documents_files:
            for document in documents_files:
                print("fileshere")
                Document.objects.create(
                    document=document,
                    trainer=instance,
                )
        instance.save()
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "date_of_birth",
            "profile_picture",
            "country",
            "gender",
            "phone_number",
            "created_at",
            "updated_at",
        ]


class CustomUserClubAddSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    profile_picture = Base64ImageField(required=False)

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
            "country",
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
            "country": {"required": False},
            "phone_number": {"required": True},
        }

    def validate(self, data):
        if CustomUser.objects.filter(email=data.get("email")).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if len(data.get("password", "")) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long."}
            )
        if not data.get("username"):
            raise serializers.ValidationError({"username": "Username is required."})
        return data

    def create(self, validated_data):
        validated_data.pop(
            "confirm_password"
        )  # Remove confirm_password before creating user
        print('validated_data', validated_data)
        user = CustomUser.objects.create_owner(**validated_data)
        return user


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "date_of_birth",
            "profile_picture",
            "gender",
            "country",
            "phone_number",
        ]
        extra_kwargs = {
            "username": {"required": False},
            "date_of_birth": {"required": False},
            "profile_picture": {"required": False},
            "country": {"required": False},
            "phone_number": {"required": False},
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth
        )
        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.country = validated_data.get("country", instance.country)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.save()
        return instance


# class ResetPasswordEmailRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField(min_length=2)

#     redirect_url = serializers.CharField(max_length=500, required=False)

#     class Meta:
#         fields = ["email"]


# class LogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField()

#     default_error_message = {"bad_token": ("Token is expired or invalid")}

#     def validate(self, attrs):
#         self.token = attrs["refresh"]
#         return attrs

#     def save(self, **kwargs):

#         try:
#             RefreshToken(self.token).blacklist()

#         except TokenError:
#             self.fail("bad_token")


# class RegisterSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=255, min_length=3)
#     password = serializers.CharField(max_length=68, min_length=6, write_only=True)
#     user_type = serializers.CharField(max_length=255)

#     def validate(self, attrs):
#         email = attrs.get("email", "")
#         password = attrs.get("password", "")
#         user_type = attrs.get("user_type", "")

#         if not email:
#             raise serializers.ValidationError("Email is required to register")
#         if not password:
#             raise serializers.ValidationError("Password is required to register")
#         if not user_type:
#             raise serializers.ValidationError("User type is required to register")

#         return attrs

#     def create(self, validated_data):
#         email = validated_data.pop("email", None)
#         password = validated_data.pop("password", None)
#         user_type = validated_data.pop("user_type", None)
#         if user_type == "trainer":
#             user = CustomUser.objects.create_trainer(
#                 email,
#                 password,
#             )
#             Trainer.objects.create(user=user).save()
#             return user
#         elif user_type == "trainee":
#             user = CustomUser.objects.create_trainee(
#                 email,
#                 password,
#             )
#             Trainee.objects.create(user=user).save()
#             return user
#         else:
#             raise serializers.ValidationError("Invalid user type")


# class CompleteProfileSerializer(serializers.Serializer):
#     user = CompleteProfileUserSerializer()
#     sport_field = serializers.CharField(max_length=255, required=False)

#     @swagger_auto_schema(request_body=CompleteProfileUserSerializer)
#     def validate(self, attrs):
#         user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             user = request.user
#         sport_field = attrs.get("sport_field", "")
#         if user.is_trainer() and not sport_field:
#             raise serializers.ValidationError("Sport field is required for trainers")
#         if user.is_trainee() and sport_field:
#             raise serializers.ValidationError(
#                 "Sport field is not required for trainees"
#             )
#         return attrs

#     @swagger_auto_schema(request_body=CompleteProfileUserSerializer)
#     def update(self, instance, validated_data):
#         user_data = validated_data.pop("user", {})
#         sport_field = validated_data.pop("sport_field", "")
#         user = CustomUser.objects.get(id=instance.id)
#         user_serializer = CompleteProfileUserSerializer(
#             user, data=user_data, partial=True
#         )
#         if user_serializer.is_valid():
#             user_serializer.save()
#         if instance.is_trainer():
#             trainer = Trainer.objects.get(user=user)
#             trainer.sport_field = sport_field
#             trainer.save()
#         else:
#             trainee = Trainee.objects.get(user=user)
#             trainee.save()
#         return user


# class CompleteProfileUserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = CustomUser
#         fields = [
#             "username",
#             "phone_number",
#             "date_of_birth",
#             "profile_picture",
#             "country",
#             "gender",
#         ]
#         extra_kwargs = {
#             "username": {"required": True},
#             "date_of_birth": {"required": True},
#             "profile_picture": {"required": False},
#             "country": {"required": False},
#             "phone_number": {"required": False},
#             "gender": {"required": True},
#         }

#     def update(self, instance, validated_data):
#         instance.username = validated_data.get("username", instance.username)
#         instance.date_of_birth = validated_data.get(
#             "date_of_birth", instance.date_of_birth
#         )
#         instance.profile_picture = validated_data.get(
#             "profile_picture", instance.profile_picture
#         )
#         instance.country = validated_data.get("country", instance.country)
#         instance.phone_number = validated_data.get(
#             "phone_number", instance.phone_number
#         )
#         instance.save()

#         return instance


# class CompleteProfileSerializer(serializers.Serializer):
#     user = CompleteProfileUserSerializer()
#     sport_field = serializers.CharField(max_length=255, required=False)

#     @swagger_auto_schema(request_body=CompleteProfileUserSerializer)
#     def validate(self, attrs):
#         user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             user = request.user
#         sport_field = attrs.get("sport_field", "")
#         if user.is_trainer() and not sport_field:
#             raise serializers.ValidationError("Sport field is required for trainers")
#         if user.is_trainee() and sport_field:
#             raise serializers.ValidationError(
#                 "Sport field is not required for trainees"
#             )
#         return attrs

#     @swagger_auto_schema(request_body=CompleteProfileUserSerializer)
#     def update(self, instance, validated_data):
#         user_data = validated_data.pop("user", {})
#         sport_field = validated_data.pop("sport_field", "")
#         user = CustomUser.objects.get(id=instance.id)
#         user_serializer = CompleteProfileUserSerializer(
#             user, data=user_data, partial=True
#         )
#         if user_serializer.is_valid():
#             user_serializer.save()
#         if instance.is_trainer():
#             trainer = Trainer.objects.get(user=user)
#             trainer.sport_field = sport_field
#             trainer.save()
#         return user


# class UpdatePreferenceSerializer(serializers.Serializer):
#     trainer = UpdatePreferenceTrainerSerializer(required=False)
#     trainee = UpdatePreferenceTraineeSerializer(required=False)

#     def validate(self, attrs):
#         user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             user = request.user
#         if user.is_trainer() and "trainer" not in attrs:
#             raise serializers.ValidationError(
#                 "Trainer data is required for trainer user"
#             )
#         if not user.is_trainer() and "trainee" not in attrs:
#             raise serializers.ValidationError(
#                 "Trainee data is required for trainee user"
#             )
#         return attrs

#     def update(self, instance, validated_data):
#         user = CustomUser.objects.get(id=instance.id)
#         if user.is_trainer():
#             trainer_data = validated_data.pop("trainer", {})
#             trainer = Trainer.objects.get(user=user)
#             trainer_serializer = UpdatePreferenceTrainerSerializer(
#                 trainer, data=trainer_data, partial=True
#             )
#             if trainer_serializer.is_valid():
#                 trainer_serializer.save()
#         else:
#             trainee_data = validated_data.pop("trainee", {})
#             trainee = Trainee.objects.get(user=user)
#             trainee_serializer = UpdatePreferenceTraineeSerializer(
#                 trainee, data=trainee_data, partial=True
#             )
#             if trainee_serializer.is_valid():
#                 trainee_serializer.save()
#         return user
