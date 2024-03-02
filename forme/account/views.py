# views.py
from django.shortcuts import get_object_or_404
from authentication.utils import IsAuthenticatedUser

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from trainings.models import Trainer
from .models import Trainee, CustomUser
from .serializers import TraineeProfileSerializer


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
            print("user is trainee")
            trainee_profile = get_object_or_404(Trainee, user=user)
            trainee_profile.user.profile_picture = profile_picture
            trainee_profile.user.username = username
            trainee_profile.user.phone_number = phone_number
            trainee_profile.user.gender = gender
            trainee_profile.user.location = location
            trainee_profile.user.save()
            trainee_profile.save()
            return Response("Trainee Profile Updated Successfuly", status=200)
        elif user.is_trainer():
            DOB = user_data.get("date_of_birth")
            sport_field = request.data.get("sport_field")
            if username and gender and location and DOB and sport_field:
                trainer_profile = get_object_or_404(Trainer, user=user)
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
            trainee_profile = get_object_or_404(Trainee, user=user)
            date_of_birth = request.data.get("user").get("date_of_birth")
            weight = request.data.get("weight")
            height = request.data.get("height")
            fitness_goals = request.data.get("fitness_goals")
            current_physical_level = request.data.get("current_physical_level")
            if (
                date_of_birth
                and weight
                and height
                and fitness_goals
                and current_physical_level
            ):
                trainee_profile.user.date_of_birth = date_of_birth
                trainee_profile.weight = weight
                trainee_profile.height = height
                trainee_profile.fitness_goals = fitness_goals
                trainee_profile.current_physical_level = current_physical_level
                trainee_profile.user.save()
                trainee_profile.save()
                return Response("Trainee Profile Updated Successfuly", status=200)
            else:
                return Response({"detail": "Invalid data provided"}, status=400)
        elif user.is_trainer():
            trainer_profile = get_object_or_404(Trainer, user=user)
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


# Create your views here.
@api_view(["GET"])
def TraineeProfileList(request):
    trainee_profiles = Trainee.objects.all()
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
    trainee_profile = get_object_or_404(Trainee, pk=pk)

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
