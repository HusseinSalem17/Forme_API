# views.py

from rest_framework import generics
from .models import TraineeProfile, Rating, TrainerProfile, Owner
from .serializers import (
    TraineeProfileSerializer,
)
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes


@api_view(["GET"])
def TraineeProfileList(request):
    trainee_profiles = TraineeProfile.objects.all()
    serializer = TraineeProfileSerializer(trainee_profiles, many=True)
    return Response(serializer.data)


class TraineeProfileListCreateView(generics.ListCreateAPIView):
    queryset = TraineeProfile.objects.all()
    serializer_class = TraineeProfileSerializer

    def get_queryset(self):
        queryset = TraineeProfile.objects.all()
        return queryset.select_related("user__trainer_profile")


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
