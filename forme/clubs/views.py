from authentication.utils import IsAuthenticatedUser
from account.serializers import (
    CustomUserClubPostSerializer,
    CustomUserClubPutSerializer,
)
from trainings.serializers import ReviewsDetailSerializer
from trainings.models import Trainer
from .serializers import (
    BranchDetailSerializer,
    BranchGallerySerializer,
    BranchListSerializer,
    BranchMemberSerializer,
    BranchPostSerializer,
    BranchPutSerializer,
    BranchTrainerPutSerializer,
    BranchTrainerSerializer,
    ClubPostSerializer,
    ClubPutSerializer,
    ClubsListSerializer,
    NewTrainerPostSerializer,
    NewTrainerPutSerializer,
    NewTrainerSerializer,
    SubscriptionPlanPutSerializer,
    SubscriptionPostSerializer,
    SubscriptionPutSerializer,
    SubscriptionSerializer,
)
from .models import (
    Branch,
    BranchGallery,
    BranchMember,
    BranchTrainer,
    Club,
    NewTrainer,
    Subscription,
    SubscriptionPlan,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
# def get_nearest_clubs():
#     clubs = Owner.objects.all()
#     serializer = OwnerDetailSerializer(clubs, many=True)
#     return serializer.data


@api_view(["POST"])
def register_branch(request):
    try:

        if request.method == "POST":
            owner_data = request.data.get("owner", {})
            club_data = request.data.get("club", {})
            branch_data = request.data.get("branch", {})
            # Validate the owner data
            owner_serializer = CustomUserClubPostSerializer(data=owner_data)
            if not owner_serializer.is_valid():
                return Response(
                    owner_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            # Validate the club data
            club_serializer = ClubPostSerializer(data=club_data)
            if not club_serializer.is_valid():
                return Response(
                    club_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            # Validate the branch data
            branch_serializer = BranchPostSerializer(data=branch_data)
            if not branch_serializer.is_valid():
                return Response(
                    branch_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            # create the owner
            owner = owner_serializer.save()
            # create the club
            club = club_serializer.save()
            # create the branch
            branch = branch_serializer.save(owner=owner, club=club)

            return Response(
                {"message": "Branch registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("error7", e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@permission_classes([IsAuthenticatedUser])
def edit_branch(request):
    try:
        branch = Branch.objects.get(owner=request.user)
    except Branch.DoesNotExist:
        return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)
    print("here")
    if request.method == "PUT":
        data = request.data
        if "owner" in data:
            owner_serializer = CustomUserClubPutSerializer(
                branch.owner, data=data["owner"], partial=True
            )
            print("owner")
            if owner_serializer.is_valid():
                owner_serializer.save()
            else:
                return Response(
                    owner_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            data.pop("owner")

        if "club" in data:
            club_serializer = ClubPutSerializer(
                branch.club, data=data["club"], partial=True
            )
            if club_serializer.is_valid():
                club_serializer.save()
            else:
                return Response(
                    club_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            data.pop("club")

        serializer = BranchPutSerializer(branch, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Branch updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def branch_detail(request):
    owner = request.user
    branch = Branch.objects.filter(owner=owner)
    if request.method == "GET":
        serializer = BranchDetailSerializer(branch, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def branch_trainers(request):
    owner = request.user
    branch = Branch.objects.filter(owner=owner)
    if request.method == "GET":
        trainers = branch.values("trainers")
        trainers = BranchTrainer.objects.filter(id__in=trainers)
        print("heremember", trainers)
        serializer = BranchTrainerSerializer(trainers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def get_new_trainers(request):
    owner = request.user
    branch = Branch.objects.filter(owner=owner).first()
    new_trainers = NewTrainer.objects.filter(branch=branch)
    if request.method == "GET":
        serializer = NewTrainerSerializer(new_trainers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def get_branch_trainers(request):
    try:
        branch_trainers_response = branch_trainers(request)
        new_trainers_response = get_new_trainers(request)

        # Combine responses into a single response
        combined_response_data = {
            "existing_trainers": branch_trainers_response.data,
            "new_trainers": new_trainers_response.data,
        }

        return Response(combined_response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def add_existing_trainer(request, slug):
    owner = request.user
    branch = Branch.objects.filter(owner=owner).first()
    trainer = Trainer.objects.filter(slug=slug).first()
    if not trainer:
        return Response(
            {"error": "Trainer not found"}, status=status.HTTP_404_NOT_FOUND
        )
    trainer = BranchTrainer.objects.create(trainer=trainer)
    if not branch:
        return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)
    branch.trainers.add(trainer)
    return Response(
        {"message": "Trainer added successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticatedUser])
def edit_existing_trainer(request, id):
    if request.method in ["PUT", "PATCH"]:
        branch_trainer = BranchTrainer.objects.get(id=id)
        serializer = BranchTrainerPutSerializer(
            branch_trainer,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Branch trainer updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticatedUser])
def delete_existing_trainer(request, id):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        branch_trainer = BranchTrainer.objects.get(id=id)
        if request.method == "DELETE" and branch_trainer in branch.trainers.all():
            branch_trainer.delete()
            return Response(
                {"message": "Branch trainer deleted successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except BranchTrainer.DoesNotExist:
        return Response(
            {"error": "Branch trainer not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def add_new_trainer(request):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        if request.method == "POST":
            serializer = NewTrainerPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(branch=branch)
                return Response(
                    {"message": "Trainer added successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticatedUser])
def edit_new_trainer(request, id):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        if request.method == "PUT" or request.method == "PATCH":
            trainer = NewTrainer.objects.get(id=id)
            serializer = NewTrainerPutSerializer(trainer, data=request.data)
            if serializer.is_valid():
                serializer.save(branch=branch)
                return Response(
                    {"message": "Trainer updated successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticatedUser])
def delete_new_trainer(request, id):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        trainer = NewTrainer.objects.get(id=id)
        if request.method == "DELETE" and trainer.branch == branch:
            trainer.delete()
            return Response(
                {"message": "Trainer deleted successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except NewTrainer.DoesNotExist:
        return Response(
            {"error": "Trainer not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def branch_members(request):
    owner = request.user
    branch = Branch.objects.filter(owner=owner)
    if request.method == "GET":
        members = branch.values("members")
        members = BranchMember.objects.filter(id__in=members)
        print("heremember", members)
        serializer = BranchMemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def branch_subscriptions(request):
    try:
        owner = request.user
        branch = Branch.objects.filter(
            owner=owner
        ).first()  # Use .first() to get a single branch
        if not branch:
            return Response(
                {"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND
            )

        subscriptions = Subscription.objects.filter(branch=branch)
        if request.method == "GET":
            serializer = SubscriptionSerializer(subscriptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def create_branch_subscription(request):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        if request.method == "POST":
            serializer = SubscriptionPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(branch=branch)
                return Response(
                    {"message": "Subscription added successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticatedUser])
def edit_branch_subscription(request, id):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        subscription = Subscription.objects.get(id=id)
        if (
            request.method == "PUT" or request.method == "PATCH"
        ) and subscription.branch == branch:
            serializer = SubscriptionPutSerializer(subscription, data=request.data)
            if serializer.is_valid():
                serializer.save(branch=branch)
                return Response(
                    {"message": "Subscription updated successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticatedUser])
def delete_branch_subscription(request, id):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        subscription = Subscription.objects.get(id=id)
        if request.method == "DELETE" and subscription.branch == branch:
            subscription.delete()
            return Response(
                {"message": "Subscription deleted successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Subscription.DoesNotExist:
        return Response(
            {"error": "Subscription not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticatedUser])
def edit_branch_subscription_plan(request, duration):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        subscription_plan = SubscriptionPlan.objects.get(duration=duration)
        if (
            request.method in ["PUT", "PATCH"]
            and subscription_plan.subscription.branch == branch
        ):
            serializer = SubscriptionPlanPutSerializer(
                subscription_plan, data=request.data
            )
            if serializer.is_valid():
                serializer.save(branch=branch, is_added=True)
                return Response(
                    {"message": "Subscription plan updated successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticatedUser])
def reset_branch_subscription_plan(request, duration):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        subscription_plan = SubscriptionPlan.objects.get(duration=duration)
        if (
            request.method in ["PUT", "PATCH"]
            and subscription_plan.subscription.branch == branch
        ):
            subscription_plan.is_added = False
            subscription_plan.price = subscription_plan.subscription.price * duration
            subscription_plan.save()
            return Response(
                {"message": "Subscription plan reset successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def get_branch_galleries(request):
    owner = request.user
    branch = Branch.objects.filter(owner=owner).first()
    if request.method == "GET":
        gallery = BranchGallery.objects.filter(branch=branch)
        serializer = BranchGallerySerializer(gallery, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def add_branch_gallery(request):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        if request.method == "POST":
            serializer = BranchGallerySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(branch=branch)
                return Response(
                    {"message": "Gallery added successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticatedUser])
def delete_branch_gallery(request, id):
    try:
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        gallery = BranchGallery.objects.get(id=id)
        if request.method == "DELETE" and gallery.branch == branch:
            gallery.delete()
            return Response(
                {"message": "Gallery deleted successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except BranchGallery.DoesNotExist:
        return Response(
            {"error": "Gallery not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def get_branch_reviews(request):
    owner = request.user
    branch = Branch.objects.filter(owner=owner).first()
    if request.method == "GET":
        reviews = branch.reviews.all()
        serializer = ReviewsDetailSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
