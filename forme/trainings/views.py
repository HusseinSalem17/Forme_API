from authentication.utils import IsAuthenticatedUser

from .models import Program, Session, Workout, Trainer
from rest_framework.response import Response

from .serializers import (
    ProgramDetailSerializer,
    ProgramListSerializer,
    SessionSerializer,
    TrainerWorkoutsSerializer,
    WorkoutDetailSerializer,
    WorkoutListSerializer,
    TrainerDetailSerializer,
    TrainerListSerializer,
    TrainerProgramsSerializer,
)
from rest_framework import status


from django.shortcuts import get_object_or_404


from random import shuffle
from rest_framework.decorators import api_view, permission_classes


# Create your views here.
@api_view(["GET"])
def TrainerProfileList(request):
    trainer_profiles = Trainer.objects.all()
    if request.method == "GET":
        serializer = TrainerListSerializer(trainer_profiles, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
def TrainerProfileDetail(request, pk):
    trainer_profile = get_object_or_404(Trainer, pk=pk)

    if request.method == "GET":
        serializer = TrainerDetailSerializer(trainer_profile)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TrainerDetailSerializer(trainer_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def top_rated_trainers():
    trainers = Trainer.objects.order_by("-avg_ratings")[:10]
    serializer = TrainerListSerializer(trainers, many=True)
    return serializer.data


def get_programs_trainers():
    trainers = list(Trainer.objects.all())
    shuffle(trainers)
    serializer = TrainerProgramsSerializer(trainers, many=True)
    return serializer.data


def get_workouts_trainers():
    trainers = list(Trainer.objects.all())
    shuffle(trainers)
    serializer = TrainerWorkoutsSerializer(trainers, many=True)
    return serializer.data


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def get_programs_trainer(request):
    try:
        user = request.user
        trainer = Trainer.objects.get(user=user)
    except Trainer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        programs = Program.objects.filter(trainer=trainer)
        serializer = ProgramListSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def get_workouts_trainer(request):
    try:
        user = request.user
        trainer = Trainer.objects.get(user=user)
    except Trainer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        workouts = Workout.objects.filter(trainer=trainer)
        serializer = WorkoutListSerializer(workouts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def add_workout(request):
    if request.method == "POST":
        try:
            user = request.user
            trainer = Trainer.objects.get(user=user)
            serializer = WorkoutListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(trainer=trainer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trainer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def add_program(request):
    if request.method == "POST":
        try:
            user = request.user
            trainer = Trainer.objects.get(user=user)
            serializer = ProgramListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(trainer=trainer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trainer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticatedUser])
def update_program(request, pk):
    try:
        program = Program.objects.get(pk=pk)
    except Program.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = ProgramListSerializer(program, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticatedUser])
def update_workout(request, pk):
    try:
        workout = Workout.objects.get(pk=pk)
    except Workout.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = WorkoutListSerializer(workout, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def home(request):
    if request.method == "GET":
        data = {
            "top_trainers": top_rated_trainers(),
            "workouts": get_workouts_trainers(),
            "programs": get_programs_trainers(),
            # "nearest_clubs": get_nearest_clubs(),
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def program_list(request):
    programs = Program.objects.all()
    if request.method == "GET":
        serializer = ProgramListSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def program_detail(request, pk):
    try:
        program = Program.objects.get(pk=pk)
    except Program.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProgramDetailSerializer(program)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def workout_list(request):
    workouts = Workout.objects.all()
    if request.method == "GET":
        serializer = WorkoutListSerializer(workouts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def workout_detail(request, pk):
    try:
        workout = Workout.objects.get(pk=pk)
    except Workout.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = WorkoutDetailSerializer(workout)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def get_trainer_sessions(request, pk):
    try:
        trainer = Trainer.objects.get(pk=pk)
    except Trainer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        sessions = Session.objects.filter(trainer=trainer)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "POST"])
@permission_classes([IsAuthenticatedUser])
def add_session_settings(request):
    if request.method == "PUT":
        try:
            user = request.user
            trainer = Trainer.objects.get(user=user)
            session = Session.objects.filter(trainer=trainer).first()
            if session:
                serializer = SessionSerializer(session, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"message": "Session updated successfully"},
                        status=status.HTTP_200_OK,
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Trainer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        try:
            user = request.user
            trainer = Trainer.objects.get(user=user)
            serializer = SessionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(trainer=trainer)
                return Response(
                    {"message": "Session created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trainer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def get_trainer_data(request, trainer_id):
#     try:
#         trainer = TrainerProfile.objects.get(pk=trainer_id)
#     except TrainerProfile.DoesNotExist:
#         return Response({"error": "Trainer not found"}, status=404)

#     if request.method == "GET":
#         # Serialize trainer programs
#         trainer_programs_serializer = TrainerProgramsSerializer(trainer)
#         programs_data = trainer_programs_serializer.data

#         # Serialize trainer workouts
#         trainer_workouts_serializer = TrainerWorkoutsSerializer(trainer)
#         workouts_data = trainer_workouts_serializer.data

#         return Response(
#             {
#                 "trainer_programs": programs_data,
#                 "trainer_workouts": workouts_data,
#             },
#             status=200,
#         )
#     else:
#         return Response({"error": "Invalid request method"}, status=400)
