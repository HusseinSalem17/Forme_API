from django.shortcuts import get_object_or_404

from forme.utils import handle_validation_error
from trainings.models import Trainee, Trainer
from trainings.serializers import TraineeSerializer, TrainerSerializer

from rest_framework import status
from rest_framework import serializers
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
    VerifyOTPSerializer,
    UpdatePreferenceTrainerSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from .threads import Util
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import GenericAPIView
# from django_redis import get_redis_connection

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
        try:
            user = request.user
            print("is trainee", user.is_trainee())
            if not user.is_trainee():
                return Response(
                    {"error": "You are not a trainee"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = self.serializer_class(
                request.user,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            trainee = Trainee.objects.filter(user=user).first()
            if not trainee:
                return Response(
                    {"error": "Trainee does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(TraineeSerializer(trainee).data, status=200)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        try:
            user = request.user
            if not user.is_trainer():
                return Response(
                    {"error": "You are not a trainer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.filter(user=user).first()
            if not trainer:
                return Response(
                    {"error": "Trainer does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            print("trainer here", trainer)
            serializer = self.serializer_class(
                trainer,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            trainer = serializer.save()
            return Response(TrainerSerializer(trainer).data, status=200)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for Forget Password screen (then set new password screen)
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
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data["email"]
            Util.send_otp(email)
            return Response(
                {"message": "We have sent otp to your email!"},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for Logout
class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="For Logout",
        tags=["auth", "clubs"],
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
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print("logout serializer", serializer)
            return Response(
                {"message": "Logout successfuly"},
                status=status.HTTP_200_OK,
            )

        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
                        "message": "Password updated successfully!",
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
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            user = request.user
            if user.check_password(serializer.validated_data["old_password"]):
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response(
                    {"message": "Password updated successfully!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Old password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Util.send_otp(serializer.validated_data["email"])
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            Util.change_otp_verify(email)
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"message": "Password updated successfully!"}, status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        try:
            user = request.user
            print("user here", user.id)
            print("data here", request.data)
            location = Location.objects.get(object_id=user.id)
            serializer = self.serializer_class(
                location, data=request.data, partial=True, context={"request": request}
            )
            print("reached here")
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Save user data in Redis with a timeout of 10 minutes
            # cache_key = f"location_{user.id}"
            # cache.set(cache_key, serializer.data, ttl=600)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
        try:
            user = request.user
            location = Location.objects.get(object_id=user.id)
            serializer = self.serializer_class(location)
            # Save user data in Redis with a timeout of 10 minutes
            # cache_key = f"location_{user.id}"

            # if cache.__contains__(cache_key):
            #     cached_data = cache.get(cache_key)
            #     return Response(cached_data, status=status.HTTP_200_OK)

            # cache.set(cache_key, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Location.DoesNotExist:
            return Response(
                {"error": "Location does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        try:
            user = request.user
            if not user.is_trainee():
                return Response(
                    {"message": "You are not a trainee"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainee = Trainee.objects.get(user=user)
            serializer = self.serializer_class(
                trainee,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Preference Updated successfully!"}, status=200)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
            properties={
                "bio": openapi.Schema(type=openapi.TYPE_STRING, description="Bio"),
                "exp_injuries": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN, description="Experience in injuries"
                ),
                "physical_disabilities": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN, description="Physical disabilities"
                ),
                "id_card": openapi.Schema(
                    type=openapi.FORMAT_BASE64,
                    description="Profile picture",
                    example="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAALCAYAAAB8sKbRAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABaElEQVQ4jZ2Tz0tDQRTHv+9f7",
                ),
                "languages": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description="Languages",
                ),
                "documents": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "document": openapi.Schema(
                                type=openapi.TYPE_FILE, description="Document"
                            )
                        },
                    ),
                    description="Documents",
                ),
                "facebook_url": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Facebook URL"
                ),
                "instagram_url": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Instagram URL"
                ),
                "youtube_url": openapi.Schema(
                    type=openapi.TYPE_STRING, description="YouTube URL"
                ),
            },
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
                        "message": "Preference Updated successfully!",
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
        try:
            user = request.user
            if not user.is_trainer():
                return Response(
                    {"error": "You are not a trainer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)
            if not trainer:
                return Response(
                    {"error": "Trainer does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = self.serializer_class(
                trainer,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "Preference Updated successfully!"},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
                        "error": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error messages"
                        ),
                    },
                    example={"errors": {"user_type": ["User type is required."]}},
                ),
            ),
        },
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
                        "message": "OTP verified successfully!",
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
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(
                raise_exception=True
            )  # This will automatically raise an exception if not valid

            email = serializer.validated_data["email"]
            otp = serializer.validated_data["otp"]
            otp_obj = get_object_or_404(OTP, email=email, verified=False)
            if otp_obj.otp == int(otp):
                otp_obj.verified = True
                otp_obj.save()
                return Response({"message": "OTP verified successfully!"}, status=200)
            else:
                return Response({"error": "Incorrect otp"}, status=400)

        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
