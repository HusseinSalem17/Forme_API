from django.shortcuts import get_object_or_404

from trainings.models import Trainee, Trainer
from trainings.serializers import TraineeSerializer, TrainerSerializer

from rest_framework import status

from rest_framework.response import Response
from .models import OTP, CustomUser, Location
from .serializers import (
    CompleteProfileTrainerSerializer,
    CompleteProfileUserSerializer,
    ForgetPasswordSerializer,
    LocationSerializer,
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
    RequestOTPSerializer,
    ResetPasswordSerializer,
    SetNewPasswordSerializer,
    UpdatePreferenceTraineeSerializer,
    UploadProfilePictureSerializer,
    VerifyOTPSerializer,
    UpdatePreferenceTrainerSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import GenericAPIView
from django_redis import get_redis_connection

# cache = RedisCache(get_redis_connection("default"), ttl=600)


# for Compelete Profile Trainee Screen
class CompleteProfileTraineeView(GenericAPIView):
    serializer_class = CompleteProfileUserSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="For Complete Profile Trainee",
        tags=["profile"],
        operation_id="Complete Profile Trainee",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Username",
                    example="username",
                ),
                "country": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Location",
                ),
                "profile_picture": openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description="Profile picture",
                ),
                "phone_number": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Phone number",
                ),
                "gender": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Gender",
                ),
            },
            required=["username", "country", "gender"],
        ),
        responses={
            200: TraineeSerializer,
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def patch(self, request):
        user = request.user
        if not user.is_trainee:
            return Response(
                {"message": "You are not a trainee"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            trainee = Trainee.objects.get(user=user)
            return Response(TraineeSerializer(trainee).data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for Complete Profile Trainer Screeen
class CompleteProfileTrainerView(GenericAPIView):
    serializer_class = CompleteProfileTrainerSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="For Complete Profile Trainee",
        tags=["profile"],
        operation_id="Complete Profile Trainer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "username": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Username",
                            example="username",
                        ),
                        "date_of_birth": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Date of birth",
                            example="1990-01-01",
                        ),
                        "country": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Location",
                        ),
                        "profile_picture": openapi.Schema(
                            type=openapi.TYPE_FILE,
                            description="Profile picture",
                        ),
                        "phone_number": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Phone number",
                        ),
                        "gender": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Gender",
                        ),
                    },
                    required=["username", "date_of_birth", "country", "gender"],
                ),
                "sport_field": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Sport field"
                ),
            },
            required=["user", "sport_field"],
        ),
        responses={
            200: TrainerSerializer,
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def patch(self, request):
        user = request.user
        if not user.is_trainer:
            return Response(
                {"message": "You are not a trainer"}, status=status.HTTP_400_BAD_REQUEST
            )
        trainer = Trainer.objects.get(user=user)
        print("trainer here", trainer)
        serializer = self.serializer_class(
            trainer,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            print("reached here")
            trainer = serializer.save()
            return Response(TrainerSerializer(trainer).data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for Foget Password screen (then set new password screen)
class ForgetPasswordView(GenericAPIView):
    serializer_class = ForgetPasswordSerializer

    @swagger_auto_schema(
        operation_description="For Forget Password Screen Then verify OTP Screen then set new password request",
        request_body=ForgetPasswordSerializer,
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "We have sent otp to your email!",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp = Util.send_otp(email)
            return Response({"message": "We have sent otp to your email!"}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for Login Screen
class LoginView(GenericAPIView):

    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_description="For Login Screen",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Access token"
                        ),
                        "refresh": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Refresh token"
                        ),
                    },
                    example={
                        "access": "access_token_string",
                        "refresh": "refresh_token_string",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for Logout
class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="For Logout",
        tags=["auth","clubs"],
        request_body=LogoutSerializer,
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "Logout successfuly",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Logout successfuly"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for delete account
class DeleteAccountView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Delete User",
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "User deleted successfully",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "User deleted successfully"}, status=200)


# For Reset Password Screen
class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Reset Password Screen After Login",
        request_body=ResetPasswordSerializer,
        security=[{"Bearer": []}],
        operation_id="reset_password",
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "Password changed successfully",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def put(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data["old_password"]):
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response(
                    {"message": "Password changed successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Incorrect old password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# to request otp screen (for register)
class RequestOTPView(GenericAPIView):

    serializer_class = RequestOTPSerializer

    @swagger_auto_schema(
        operation_description="Request OTP for register Screen",
        request_body=RequestOTPSerializer,
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "We have sent otp to your email!",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Util.send_otp(serializer.validated_data["email"])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for set new password after forget password
class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    @swagger_auto_schema(
        operation_description="Set New Password after Forget Password",
        request_body=SetNewPasswordSerializer,
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "Password updated successfully",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
    )
    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            Util.change_otp_verify(email)
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "Password updated successfully"}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for location screen
class LocationView(GenericAPIView):

    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Update Location",
        tags=["Location"],
        request_body=LocationSerializer,
        operation_id="Location",
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "Location updated successfully",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={
                        "errors": {
                            "longitude": ["Longitude is required"],
                            "latitude": ["Latitude is required"],
                        }
                    },
                ),
            ),
        },
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def patch(self, request):
        user = request.user
        # user_content_type = ContentType.objects.get_for_model(user)
        # location = Location.objects.get(
        #     content_type=user_content_type, object_id=user.id
        # )
        location = Location.objects.get(object_id=user.id)
        serializer = self.serializer_class(
            location, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()

            # Save user data in Redis with a timeout of 10 minutes
            # cache_key = f"location_{user.id}"
            # cache.set(cache_key, serializer.data, ttl=600)

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Get Location",
        tags=["Location"],
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "latitude": openapi.Schema(
                            type=openapi.TYPE_NUMBER, description="Latitude"
                        ),
                        "longitude": openapi.Schema(
                            type=openapi.TYPE_NUMBER, description="Longitude"
                        ),
                    },
                    example={"latitude": 23.456, "longitude": 45.678},
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={
                        "errors": {
                            "longitude": ["Longitude is required"],
                            "latitude": ["Latitude is required"],
                        }
                    },
                ),
            ),
        },
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def get(self, request):
        user = request.user
        # user_content_type = ContentType.objects.get_for_model(user)
        # location = Location.objects.get(content_type=user_content_type, object_id=user.id)
        location = Location.objects.get(object_id=user.id)
        serializer = self.serializer_class(location)

        # Save user data in Redis with a timeout of 10 minutes
        # cache_key = f"location_{user.id}"

        # if cache.__contains__(cache_key):
        #     cached_data = cache.get(cache_key)
        #     return Response(cached_data, status=status.HTTP_200_OK)

        # cache.set(cache_key, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfilePictureView(GenericAPIView):

    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Update Profile Picture",
        request_body=UploadProfilePictureSerializer,
        tags=["profile"],
        operation_id="update_profile_picture",
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "Profile picture updated successfully",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def patch(self, request):
        user = request.user
        user.profile_picture = request.data.get("profile_picture")
        user.save()
        return Response({"message": "Profile picture updated successfully"}, status=200)


# for update preference Trainee screen
class UpdatePreferenceTraineeView(GenericAPIView):

    serializer_class = UpdatePreferenceTraineeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Update Preference for Trainee",
        tags=["profile"],
        operation_id="update_preference_trainee",
        request_body=UpdatePreferenceTraineeSerializer,
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "Preference Updated successfully",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def put(self, request):
        user = request.user
        if not user.is_trainee:
            return Response(
                {"message": "You are not a trainee"}, status=status.HTTP_400_BAD_REQUEST
            )
        trainee = Trainee.objects.get(user=user)
        serializer = self.serializer_class(
            trainee,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile Updated successfully"}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for update preference Trainer screen
class UpdatePreferenceTrainerView(GenericAPIView):

    serializer_class = UpdatePreferenceTrainerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Update Preference for Trainer",
        tags=["profile"],
        operation_id="update_preference_trainer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="Trainer",
            properties={
                "bio": openapi.Schema(type=openapi.TYPE_STRING, description="Bio"),
                "exp_injuries": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Experience in injuries",
                    example=True,
                ),
                "physical_disabilities": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Physical disabilities",
                    example=True,
                ),
                "languages": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="Languages",
                    example=["English", "Arabic"],
                ),
                "id_card": openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description="ID card",
                    example="id_card.jpg",
                ),
                "document_files": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Document files",
                    items=openapi.Items(type=openapi.TYPE_FILE),
                    example=["document1.jpg", "document2.jpg"],
                ),
                "facebook_url": openapi.Schema(
                    type=openapi.FORMAT_URI,
                    description="Facebook URL",
                    example="https://www.facebook.com/",
                ),
                "instagram_url": openapi.Schema(
                    type=openapi.FORMAT_URI,
                    description="Instagram URL",
                    example="https://www.instagram.com/",
                ),
                "youtube_url": openapi.Schema(
                    type=openapi.FORMAT_URI,
                    description="Youtube URL",
                    example="https://www.youtube.com/",
                ),
            },
            required=["exp_injuries", "physical_disabilities"],
        ),
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "Preference Updated successfully",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def put(self, request):
        user = request.user
        if not user.is_trainer:
            return Response({"message": "You are not a trainer"}, status=400)
        trainer = Trainer.objects.get(user=user)
        serializer = self.serializer_class(
            trainer,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile Updated successfully"}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for register screen
class RegisterView(GenericAPIView):

    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_description="Register new user after OTP verification",
        request_body=RegisterSerializer,
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Access token"
                        ),
                        "refresh": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Refresh token"
                        ),
                    },
                    example={
                        "access": "access_token_string",
                        "refresh": "refresh_token_string",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
    )
    def post(self, request):
        if not Util.check_otp_verified(request.data["email"]):
            return Response({"message": "Please verify your OTP first"}, status=400)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    }
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for verify otp screen
class VerifyOTPView(GenericAPIView):
    serializer_class = VerifyOTPSerializer

    @swagger_auto_schema(
        operation_description="For Verify OTP Screen",
        request_body=VerifyOTPSerializer,
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                    },
                    example={
                        "message": "otp verified successfully",
                    },
                ),
            ),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp = serializer.validated_data["otp"]
            otp_obj = get_object_or_404(OTP, email=email, verified=False)
            if otp_obj.otp == int(otp):
                otp_obj.verified = True
                otp_obj.save()
                return Response({"message": "otp verified successfully"}, status=200)
            else:
                return Response({"message": "Incorrect otp"}, status=400)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RegisterView(GenericAPIView):
#     @swagger_auto_schema(
#         operation_description="Register",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "email": openapi.Schema(
#                     title="Email",
#                     default="example@example.com",
#                     type=openapi.TYPE_STRING,
#                     description="Email address",
#                 ),
#                 "password": openapi.Schema(
#                     title="Password",
#                     default="password",
#                     type=openapi.TYPE_STRING,
#                     description="Password",
#                 ),
#                 "user_type": openapi.Schema(
#                     title="User Type",
#                     default="trainee",
#                     type=openapi.TYPE_STRING,
#                     description="User type (trainer or trainee)",
#                     enum=["trainer", "trainee"],
#                 ),
#             },
#         ),
#         responses={
#             200: openapi.Response(
#                 "OK",
#                 schema=openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         "message": openapi.Schema(
#                             type=openapi.TYPE_STRING, description="Success message"
#                         ),
#                     },
#                     example={
#                         "message": "OTP sent successfully",
#                     },
#                 ),
#             ),
#             400: openapi.Response(
#                 "Bad Request",
#                 schema=openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         "message": openapi.Schema(
#                             type=openapi.TYPE_STRING, description="Error message"
#                         ),
#                     },
#                     example={"message": "Invalid data provided"},
#                 ),
#             ),
#         },
#     )
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data["email"]
#             password = serializer.validated_data["password"]
#             user_type = serializer.validated_data["user_type"]

#             # Save user data in Redis with a timeout of 10 minutes
#             cache = RedisCache(get_redis_connection("default"), ttl=600)
#             cache_key = email
#             cache[cache_key] = {
#                 "email": email,
#                 "password": password,
#                 "user_type": user_type,
#             }

#             # Send OTP to the user's email
#             Util.send_otp(email)

#             return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class VerifyOTPView(GenericAPIView):
#     serializer_class = RegisterVerifySerializer
#     #

#     @swagger_auto_schema(
#         operation_description="Verify OTP",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "email": openapi.Schema(
#                     type=openapi.TYPE_STRING, description="Email address"
#                 ),
#                 "otp": openapi.Schema(type=openapi.TYPE_STRING, description="OTP"),
#             },
#         ),
#         responses={
#             200: openapi.Response(
#                 "OK",
#                 schema=openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         "message": openapi.Schema(
#                             type=openapi.TYPE_STRING, description="Success message"
#                         ),
#                     },
#                     example={
#                         "message": "otp verified successfully",
#                     },
#                 ),
#             ),
#             400: "Invalid data",
#         },
#     )
#     def post(self, request):
#         email = request.data.get("email")
#         otp = request.data.get("otp")
#         if email and otp:
#             otp_obj = get_object_or_404(OTP, email=email, verified=False)
#             if otp_obj.validity.replace(tzinfo=None) > datetime.datetime.utcnow():
#                 print(otp_obj.validity, otp_obj.otp)
#                 if otp_obj.otp == int(otp):
#                     otp_obj.verified = True
#                     otp_obj.save()
#                     # Retrieve user data from Redis
#                     cache = RedisCache(get_redis_connection("default"))
#                     user_data = cache.get(email)
#                     if user_data:
#                         serializer = self.serializer_class(data=user_data)
#                         if serializer.is_valid():
#                             user = serializer.save()
#                             refresh = RefreshToken.for_user(user)
#                             return Response(
#                                 {
#                                     "access": str(refresh.access_token),
#                                     "refresh": str(refresh),
#                                 }
#                             )
#                         else:
#                             return Response(
#                                 serializer.errors, status=status.HTTP_400_BAD_REQUEST
#                             )
#                     else:
#                         return Response(
#                             {"message": "User data not found in Redis."},
#                             status=status.HTTP_404_NOT_FOUND,
#                         )
#                 else:
#                     return Response({"message": "Incorrect otp"}, status=400)
#             else:
#                 return Response({"message": "otp expired"}, status=400)
#         else:
#             return Response({"message": "Invalid data provided"}, status=400)

# class ResendOTPView(GenericAPIView):
#

#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "email": openapi.Schema(
#                     title="Email",
#                     default="example@example.com",
#                     type=openapi.TYPE_STRING,
#                     description="Email address",
#                 ),
#             },
#         ),
#         responses={
#             200: openapi.Response(
#                 "OK",
#                 schema=openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         "message": openapi.Schema(
#                             type=openapi.TYPE_STRING, description="Success message"
#                         ),
#                     },
#                     example={
#                         "message": "We have sent otp to your email!",
#                     },
#                 ),
#             ),
#             400: "Invalid data",
#         },
#     )
#     def post(self, request):
#         email = request.data.get("email")
#         if email:
#             return Util.send_otp(email)
#         else:
#             return Response({"detail": "Invalid data provided"}, status=400)


# class CompleteProfileView(GenericAPIView):
#     serializer_class = CompleteProfileSerializer
#
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     @swagger_auto_schema(
#         operation_description="For Complete Profile",
#         tags=["Profile"],
#         operation_id="Complete Profile",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "user": openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         "username": openapi.Schema(
#                             type=openapi.TYPE_STRING,
#                             description="Username",
#                             example="username",
#                         ),
#                         "date_of_birth": openapi.Schema(
#                             type=openapi.TYPE_STRING,
#                             description="Date of birth",
#                             example="1990-01-01",
#                         ),
#                         "location": openapi.Schema(
#                             type=openapi.TYPE_STRING,
#                             description="Location",
#                         ),
#                         "profile_picture": openapi.Schema(
#                             type=openapi.TYPE_FILE,
#                             description="Profile picture",
#                         ),
#                         "phone_number": openapi.Schema(
#                             type=openapi.TYPE_STRING,
#                             description="Phone number",
#                         ),
#                         "gender": openapi.Schema(
#                             type=openapi.TYPE_STRING,
#                             description="Gender",
#                         ),
#                     },
#                     required=["username", "date_of_birth", "location", "gender"],
#                 ),
#                 "sport_field": openapi.Schema(
#                     type=openapi.TYPE_STRING, description="Sport field"
#                 ),
#             },
#             required=["user"],
#         ),
#         responses={
#             200: openapi.Response(
#                 "OK",
#                 schema=openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         "message": openapi.Schema(
#                             type=openapi.TYPE_STRING, description="Success message"
#                         ),
#                     },
#                     example={
#                         "message": "Profile Completed successfully",
#                     },
#                 ),
#             ),
#             400: openapi.Response(
#                 "Bad Request",
#                 schema=openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         "errors": openapi.Schema(
#                             type=openapi.TYPE_OBJECT, description="Error messages"
#                         ),
#                     },
#                     example={"errors": {"user_type": ["User type is required."]}},
#                 ),
#             ),
#         },
#         security=[{"Bearer": []}],
#         manual_parameters=[
#             openapi.Parameter(
#                 "Authorization",
#                 openapi.IN_HEADER,
#                 description="Bearer <token>",
#                 type=openapi.TYPE_STRING,
#                 required=True,
#             ),
#         ],
#     )
#     def patch(self, request):
#         serializer = self.serializer_class(
#             request.user, data=request.data, partial=True, context={"request": request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Profile Completed successfully"}, status=200)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UpdatePreferenceView(GenericAPIView):
#
#     serializer_class = UpdatePreferenceSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     @swagger_auto_schema(
#         operation_description="Update Preference",
#         tags=["Profile"],
#         operation_id="update_preference",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "trainer": openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     description="Trainer",
#                     properties={
#                         "bio": openapi.Schema(
#                             type=openapi.TYPE_STRING, description="Bio"
#                         ),
#                         "exp_injuries": openapi.Schema(
#                             type=openapi.TYPE_STRING,
#                             description="Experience in injuries",
#                         ),
#                         "physical_disabilities": openapi.Schema(
#                             type=openapi.TYPE_STRING,
#                             description="Physical disabilities",
#                         ),
#                         "languages": openapi.Schema(
#                             type=openapi.TYPE_ARRAY,
#                             items=openapi.Items(type=openapi.TYPE_STRING),
#                             description="Languages",
#                         ),
#                         "id_card": openapi.Schema(
#                             type=openapi.TYPE_FILE,
#                             description="ID card",
#                         ),
#                         "document_files": openapi.Schema(
#                             type=openapi.TYPE_ARRAY,
#                             description="Document files",
#                             items=openapi.Items(type=openapi.TYPE_FILE),
#                         ),
#                         "facebook_url": openapi.Schema(
#                             type=openapi.FORMAT_URI,
#                             description="Facebook URL",
#                         ),
#                         "instagram_url": openapi.Schema(
#                             type=openapi.FORMAT_URI,
#                             description="Instagram URL",
#                         ),
#                         "youtube_url": openapi.Schema(
#                             type=openapi.FORMAT_URI,
#                             description="Youtube URL",
#                         ),
#                     },
#                     required=["exp_injuries", "physical_disabilities"],
#                 ),
#                 "trainee": openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     description="Trainee",
#                     properties={
#                         "user": openapi.Schema(
#                             type=openapi.TYPE_OBJECT,
#                             description="User",
#                             properties={
#                                 "date_of_birth": openapi.Schema(
#                                     type=openapi.FORMAT_DATE,
#                                     description="Date of birth",
#                                     example="1990-01-01",
#                                 ),
#                             },
#                             required=["date_of_birth"],
#                         ),
#                         "height": openapi.Schema(
#                             type=openapi.TYPE_NUMBER, description="Height"
#                         ),
#                         "weight": openapi.Schema(
#                             type=openapi.TYPE_NUMBER, description="Weight"
#                         ),
#                         "fitness_goals": openapi.Schema(
#                             type=openapi.TYPE_STRING, description="Fitness goals"
#                         ),
#                         "current_physical_level": openapi.Schema(
#                             type=openapi.TYPE_STRING,
#                             description="Current physical level",
#                         ),
#                     },
#                     required=[
#                         "user",
#                         "height",
#                         "weight",
#                         "fitness_goals",
#                         "current_physical_level",
#                     ],
#                 ),
#             },
#             required=["sport_field"],
#         ),
#         responses={
#             200: openapi.Response(
#                 "OK",
#                 schema=openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         "message": openapi.Schema(
#                             type=openapi.TYPE_STRING, description="Success message"
#                         ),
#                     },
#                     example={
#                         "message": "Preference Updated successfully",
#                     },
#                 ),
#             ),
#             400: openapi.Response(
#                 "Bad Request",
#                 schema=openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         "errors": openapi.Schema(
#                             type=openapi.TYPE_OBJECT, description="Error messages"
#                         ),
#                     },
#                     example={"errors": {"user_type": ["User type is required."]}},
#                 ),
#             ),
#         },
#         security=[{"Bearer": []}],
#         manual_parameters=[
#             openapi.Parameter(
#                 "Authorization",
#                 openapi.IN_HEADER,
#                 description="Bearer <token>",
#                 type=openapi.TYPE_STRING,
#                 required=True,
#             )
#         ],
#     )
#     def put(self, request):
#         serializer = self.serializer_class(
#             request.user,
#             data=request.data,
#             partial=True,
#             context={"request": request},
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Profile Updated successfully"}, status=200)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
