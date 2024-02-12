# views.py
import datetime
from django.shortcuts import get_object_or_404

from account.utils import IsAuthenticatedUser, send_otp, token_response
from .models import OTP, CustomUser, TraineeProfile, TrainerProfile, Owner
from .serializers import (
    TraineeProfileSerializer,
    TrainerProfileDetailSerializer,
    TrainerProfileListSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser, TraineeProfile, TrainerProfile

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


@api_view(["POST"])
def request_otp(request):
    email = request.data.get("email")

    if email:
        if CustomUser.objects.filter(email=email).exists():
            return Response({"detail": "email already exists"}, status=400)
        return send_otp(email)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
def resend_otp(request):
    email = request.data.get("email")
    if email:
        return send_otp(email)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
def verify_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    if email and otp:
        otp_obj = get_object_or_404(OTP, email=email, verified=False)
        if otp_obj.validity.replace(tzinfo=None) > datetime.datetime.utcnow():
            print(otp_obj.validity, otp_obj.otp)
            if otp_obj.otp == int(otp):
                otp_obj.verified = True
                otp_obj.save()
                return Response("otp verified successfully",status=200)
            else:
                print(otp_obj.otp, otp)
                return Response({"detail": "Incorrect otp"}, status=400)
        else:
            return Response({"detail": "otp expired"}, status=400)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
def reset_password(request):
    email = request.data.get("email")
    new_password = request.data.get("new_password")

    if email and new_password:
        user = get_object_or_404(CustomUser, email=email)
        user.set_password(new_password)
        user.save()
        return Response("Password reset successfully", status=200)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
def create_account(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user_type = request.data.get("user_type")

    if user_type and email and password:
        try:
            if user_type == "trainer":
                user = CustomUser.objects.create_trainer(
                    email,
                    password,
                )
                TrainerProfile.objects.create(
                    user=user,
                )
            elif user_type == "trainee":
                user = CustomUser.objects.create_trainee(
                    email,
                    password,
                )
                TraineeProfile.objects.create(
                    user=user,
                )
            return token_response(user)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email and password:
        user = get_object_or_404(CustomUser, email=email)
        if user and user.check_password(password):
            return token_response(user)
        else:
            return Response({"detail": "Invalid credentials"}, status=400)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def complete_profile(request):
    try:
        user = request.user
        user_data = request.data.get("user")  # Extract user data from the request
        profile_picture = user_data.get("profile_picture")
        username = user_data.get("username")
        phone_number = user_data.get("phone_number")
        location = user_data.get("location")
        gender = user_data.get("gender")

        if user.is_trainee() and username and gender and location:
            trainee_profile = get_object_or_404(TraineeProfile, user=user)
            trainee_profile.user.profile_picture = profile_picture
            trainee_profile.user.username = username
            trainee_profile.user.phone_number = phone_number
            trainee_profile.user.gender = gender
            trainee_profile.user.location = location
            trainer_profile.user.save()
            trainee_profile.save()
            return Response("Trainee Profile Updated Successfuly", status=200)
        elif user.is_trainer():
            DOB = user_data.get("date_of_birth")
            sport_field = request.data.get("sport_field")
            if username and gender and location and DOB and sport_field:
                trainer_profile = get_object_or_404(TrainerProfile, user=user)
                trainer_profile.user.profile_picture = profile_picture
                trainer_profile.user.username = username
                trainer_profile.user.phone_number = phone_number
                trainer_profile.user.gender = gender
                trainer_profile.user.location = location
                trainer_profile.sport_field = sport_field
                trainer_profile.user.date_of_birth = DOB
                trainer_profile.user.save()
                trainer_profile.save()
                return Response("Trainer Profile Updated Successfuly", status=200)
        else:
            return Response({"detail": "Invalid data provided"}, status=400)

    except CustomUser.DoesNotExist:
        return Response("User not found", status=404)


@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def update_preference(request):
    try:
        user = request.user
        if user.is_trainee():
            trainee_profile = get_object_or_404(TraineeProfile, user=user)
            date_of_birth = request.data.get("user").get("date_of_birth")
            weight = request.data.get("weight")
            height = request.data.get("height")
            fitness_goals = request.data.get("fitness_goals")
            current_fitness_level = request.data.get("current_fitness_level")
            if (
                date_of_birth
                and weight
                and height
                and fitness_goals
                and current_fitness_level
            ):
                trainee_profile.user.date_of_birth = date_of_birth
                trainee_profile.weight = weight
                trainee_profile.height = height
                trainee_profile.fitness_goals = fitness_goals
                trainee_profile.current_fitness_level = current_fitness_level
                trainee_profile.user.save()
                trainee_profile.save()
                return Response("Trainee Profile Updated Successfuly", status=200)
            else:
                return Response({"detail": "Invalid data provided"}, status=400)
        elif user.is_trainer():
            trainer_profile = get_object_or_404(TrainerProfile, user=user)
            bio = request.data.get("bio")
            exp_injuries = request.data.get("exp_injuries")
            physical_disabilities = request.data.get("physical_disabilities")
            languages = request.data.get("languages")
            facebook_url = request.data.get("facebook_url")
            instagram_url = request.data.get("facebook_url")
            youtube_url = request.data.get("youtube_url")
            id_card = request.data.get("id_card")
            document_files = request.data.get("document_files")
            if (
                bio
                or exp_injuries
                or physical_disabilities
                or languages
                or facebook_url
                or instagram_url
                or youtube_url
                or id_card
                or document_files
            ):
                trainer_profile.bio = bio
                trainer_profile.exp_injuries = exp_injuries
                trainer_profile.physical_disabilities = physical_disabilities
                trainer_profile.languages = languages
                trainer_profile.facebook_url = facebook_url
                trainer_profile.instagram_url = instagram_url
                trainer_profile.youtube_url = youtube_url
                trainer_profile.id_card = id_card
                trainer_profile.document_files = document_files
                trainee_profile.save()
                return Response("Trainer Profile Updated Successfuly", status=200)

            else:
                return Response({"detail": "Invalid data provided"}, status=400)
        else:
            return Response({"detail": "Invaild user type"})
    except CustomUser.DoesNotExist:
        return Response("User not found", status=404)

@api_view(["GET"])
def TraineeProfileList(request):
    trainee_profiles = TraineeProfile.objects.all()
    try:
        if request.method == "GET":
            serializer = TraineeProfileSerializer(trainee_profiles, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET", "PUT"])
def TraineeProfileDetail(request, pk):
    trainee_profile = get_object_or_404(TraineeProfile, pk=pk)

    if request.method == "GET":
        serializer = TraineeProfileSerializer(trainee_profile)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TraineeProfileSerializer(trainee_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def TrainerProfileList(request):
    trainer_profiles = TrainerProfile.objects.all()
    if request.method == "GET":
        serializer = TrainerProfileListSerializer(trainer_profiles, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
def TrainerProfileDetail(request, pk):
    trainer_profile = get_object_or_404(TrainerProfile, pk=pk)

    if request.method == "GET":
        serializer = TrainerProfileDetailSerializer(trainer_profile)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TrainerProfileDetailSerializer(trainer_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
