from .serializers import (
    BranchListSerializer,
    ClubsListSerializer,
    OwnerDetailSerializer,
)
from .models import Branch, Club, Owner
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
def get_nearest_clubs():
    clubs = Owner.objects.all()
    serializer = OwnerDetailSerializer(clubs, many=True)
    return serializer.data


@api_view(["GET"])
def club_list(request):
    clubs = Club.objects.all()
    if request.method == "GET":
        serializer = ClubsListSerializer(clubs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def branch_list(request):
    branches = Branch.objects.all()
    if request.method == "GET":
        serializer = BranchListSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
