# views.py

from webbrowser import get
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import TraineeProfile, TrainerProfile, Owner
from .serializers import (
    TraineeProfileSerializer,
    TrainerProfileSerializer,
)
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


@api_view(["GET"])
def TraineeProfileList(request):
    trainee_profiles = TraineeProfile.objects.all()
    if request.method == "GET":
        serializer = TraineeProfileSerializer(trainee_profiles, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
        serializer = TrainerProfileSerializer(trainer_profiles, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
def TrainerProfileDetail(request, pk):
    trainer_profile = get_object_or_404(TrainerProfile, pk=pk)

    if request.method == "GET":
        serializer = TrainerProfileSerializer(trainer_profile)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TrainerProfileSerializer(trainer_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



# class TraineeProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TraineeProfile.objects.all()
#     serializer_class = TraineeProfileSerializer


# class RatingListCreateView(generics.ListCreateAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer


# class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer


# class TrainerProfileListCreateView(generics.ListCreateAPIView):
#     queryset = TrainerProfile.objects.all()
#     serializer_class = TrainerProfileSerializer


# class TrainerProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TrainerProfile.objects.all()
#     serializer_class = TrainerProfileSerializer


# class OwnerListCreateView(generics.ListCreateAPIView):
#     queryset = Owner.objects.all()
#     serializer_class = OwnerSerializer


# class OwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Owner.objects.all()
#     serializer_class = OwnerSerializer
