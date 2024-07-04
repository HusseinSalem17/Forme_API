from authentication.models import CustomUser

from authentication.serializers import CustomUserSerializer, CustomUserUpdateSerializer
from forme.utils import handle_validation_error
from trainings.serializers import (
    PaymentAddSerializer,
    PaymentSerializer,
    ReviewsDetailSerializer,
)
from trainings.models import Trainee, Trainer
from .serializers import (
    AttendanceSerializer,
    AttendanceUpdateSerializer,
    BranchAddSerializer,
    BranchDetailSerializer,
    BranchGalleryAddSerializer,
    BranchGallerySerializer,
    BranchListSerializer,
    BranchLoginSerializer,
    BranchMemberJoinSerializer,
    BranchMemberSerializer,
    MemberSubscriptionUpdateSerializer,
    BranchTrainerUpdateSerializer,
    BranchTrainerSerializer,
    BranchUpdateSerializer,
    ClubsListSerializer,
    MemberSubscriptionSerializerTemp,
    NewTrainerAddSerializer,
    NewTrainerConvertSerializer,
    NewTrainerUpdateSerializer,
    NewTrainerSerializer,
    SubscriptionAddSerializer,
    SubscriptionUpdateSerializer,
    SubscriptionSerializer,
    TraineeBranchDetailSerializer,
    TrainerExistingAddSerializer,
    TrainerExistingUpdateSerializer,
)
from .models import (
    Attendance,
    Branch,
    BranchGallery,
    BranchMember,
    BranchTrainer,
    Club,
    MemberSubscription,
    NewTrainer,
    Subscription,
    SubscriptionPlan,
    Time,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from django.db.models import Min

from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncWeek

from datetime import datetime

from dateutil.relativedelta import relativedelta


# -----------------CLUBS-----------------#


# for attendance update (club)
class AttendanceUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = AttendanceUpdateSerializer

    @swagger_auto_schema(
        tags=["Trainee App"],
        operation_description="Update the attendance of a trainee",
        request_body=AttendanceUpdateSerializer,
        responses={
            200: AttendanceSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": "This field is required"},
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
    def put(self, request, attendance_id):
        try:
            user = request.user
            if not user.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            attendance = Attendance.objects.filter(id=attendance_id).first()
            if not attendance:
                return Response(
                    {"error": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(
                attendance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            attendance = serializer.save()
            return Response(
                AttendanceSerializer(attendance).data,
                status=status.HTTP_200_OK,
            )
        except Attendance.DoesNotExist:
            return Response(
                {"error": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch delete (club)
class BranchDeleteView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete the branch account",
        operation_id="Branch Delete",
        tags=["clubs"],
        responses={
            200: BranchDetailSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def delete(self, request):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.get(owner=owner)
            branch.delete()
            return Response(
                {"message": "Branch deleted successfully"}, status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch detail (club)
class BranchDetailView(GenericAPIView):
    serializer_class = BranchDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the branch details",
        tags=["clubs"],
        responses={
            200: BranchDetailSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def get(self, request):
        try:
            owner = request.user
            if not owner.is_owner():
                print("hereee now")
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(branch)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch login (club)
class BranchLoginView(GenericAPIView):
    serializer_class = BranchLoginSerializer

    @swagger_auto_schema(
        request_body=BranchLoginSerializer,
        operation_description="Login to the branch account",
        tags=["clubs"],
        operation_id="Branch Login",
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
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
            ),
        },
    )
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = CustomUser.objects.get(email=serializer.validated_data["email"])
            tokens = user.tokens()
            return Response(
                {
                    "access": str(tokens["access"]),
                    "refresh": str(tokens["refresh"]),
                }
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch register (club)
class BranchRegisterView(GenericAPIView):
    serializer_class = BranchAddSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @swagger_auto_schema(
        operation_description="Register a new branch",
        request_body=BranchAddSerializer,
        responses={
            200: BranchAddSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
            ),
        },
    )
    def post(self, request):
        try:

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # create the owner, club, and branch
            serializer.save()

            return Response(
                {"message": "Branch registered successfully, we will contact you soon"},
                status=status.HTTP_201_CREATED,
            )

        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch update (club)
class BranchUpdateView(GenericAPIView):
    serializer_class = BranchUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the branch details",
        request_body=BranchUpdateSerializer,
        tags=["clubs"],
        responses={
            200: BranchDetailSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def patch(self, request):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            print('data of request', request.data)
            serializer = self.get_serializer(branch, data=request.data, partial=True,)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            print('data of branch', branch)
            return Response(
                BranchDetailSerializer(user).data, status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# to add existing trainer (club)
class ExistingTrainerAddView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrainerExistingAddSerializer

    @swagger_auto_schema(
        tags=["clubs"],
        operation_id="Add Existing Trainer",
        operation_description="Add an existing trainer to the branch",
        request_body=TrainerExistingAddSerializer,
        responses={
            200: BranchTrainerSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
            user = request.user
            if not user.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            branch_trainer = serializer.save()
            return Response(
                BranchTrainerSerializer(branch_trainer).data,
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# for existing trainer delete (club)
class ExistingTrainerDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Delete an existing trainer from the branch",
        responses={
            200: BranchTrainerSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def delete(self, request, branch_trainer_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            # Fetch the BranchTrainer directly using trainer_id as the BranchTrainer ID
            branch_trainer = BranchTrainer.objects.get(
                id=branch_trainer_id, branch=branch
            )
            # No need to check if branch_trainer is in branch.trainers.all() since we're directly fetching it
            branch_trainer.delete()
            return Response(
                {"message": "Branch trainer deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except BranchTrainer.DoesNotExist:
            return Response(
                {"error": "Branch trainer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for existing trainer update (club)
class ExistingTrainerUpdateView(GenericAPIView):
    serializer_class = TrainerExistingUpdateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_id="Update Existing Trainer",
        operation_description="Update the details of an existing trainer",
        request_body=TrainerExistingUpdateSerializer,
        responses={
            200: BranchTrainerSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def patch(self, request, branch_trainer_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch_trainer = BranchTrainer.objects.filter(id=branch_trainer_id).first()
            if not branch_trainer:
                return Response(
                    {"error": "Branch trainer not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(
                branch_trainer, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            branch_trainer = serializer.save()
            print("reached here")
            return Response(
                BranchTrainerSerializer(branch_trainer).data, status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch galleries (club)
class BranchGalleriesView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = BranchGallerySerializer

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Get all the galleries of the branch",
        responses={
            200: BranchGallerySerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def get(self, request):
        owner = request.user
        branch = Branch.objects.filter(owner=owner).first()
        if not branch:
            return Response(
                {"error": "Branch does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        gallery = BranchGallery.objects.filter(branch=branch)
        if not gallery:
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(gallery, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# for branch gallery add (club)
class BranchGalleryAddView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = BranchGalleryAddSerializer
    
    

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Add a new gallery to the branch",
        request_body=BranchGalleryAddSerializer,
        responses={
            200: BranchDetailSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
            user = request.user
            branch = Branch.objects.filter(owner=user).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                BranchDetailSerializer(branch).data,
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch gallery delete (club)
class BranchGalleryDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Delete a gallery from the branch",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Gallery deleted successfully",
                    ),
                },
                example={"message": "Gallery deleted successfully"},
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def delete(self, request, gallery_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            gallery = BranchGallery.objects.filter(id=gallery_id).first()
            if not gallery:
                return Response(
                    {"error": "Gallery does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if gallery.branch == branch:
                gallery.delete()
                return Response(
                    {"message": "Gallery deleted successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Gallery does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch member (club)
class BranchMembersView(GenericAPIView):
    serializer_class = BranchMemberSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["clubs"],
        opearation_description="Get all the members of the branch",
        responses={
            200: BranchMemberSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def get(self, request):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            # Filter members who have at least one subscription
            members_with_subscriptions = BranchMember.objects.filter(
                branch=branch, member_subscription__isnull=False
            ).distinct()
            return Response(
                BranchMemberSerializer(members_with_subscriptions, many=True).data,
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# to delete member subscription
class MemberSubscriptionDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Delete a member subscription",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Member subscription deleted successfully",
                    ),
                },
                example={"message": "Member subscription deleted successfully"},
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def delete(self, request, member_subscription_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            subscription = MemberSubscription.objects.filter(
                id=member_subscription_id
            ).first()
            print("come hear, ", subscription)
            if not subscription:
                return Response(
                    {"error": "Member subscription not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if subscription.subscription.branch == branch:
                subscription.delete()
                print("come hear second")
                return Response(
                    {"message": "Member subscription deleted successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except MemberSubscription.DoesNotExist:
            return Response(
                {"error": "Member subscription not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# to delete branch member
class BranchMemberDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Delete a member from the branch",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Member deleted successfully",
                    ),
                },
                example={"message": "Member deleted successfully"},
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def delete(self, request, member_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            member = BranchMember.objects.get(id=member_id)
            if member.branch == branch:
                member.delete()
                return Response(
                    {"message": "Branch member deleted successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except BranchMember.DoesNotExist:
            return Response(
                {"error": "Branch member not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for new trainer add (club)
class NewTrainerAddView(GenericAPIView):
    serializer_class = NewTrainerAddSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    @swagger_auto_schema(
        tags=["clubs"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "profile_picture": openapi.Schema(type=openapi.FORMAT_BASE64),
                "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
                "subscriptions": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                ),
            },
            required=["email", "username"],
        ),
        responses={
            200: NewTrainerSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            trainer = serializer.save(branch=branch)
            return Response(
                NewTrainerSerializer(trainer).data,
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for new trainer convert (club)
class NewTrainerConvertView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = NewTrainerConvertSerializer

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Convert a new trainer to an existing trainer",
        request_body=NewTrainerConvertSerializer(),
        responses={
            200: BranchTrainerSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def post(self, request, new_trainer_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            serializer = self.get_serializer(
                data=request.data,
                context={"request": request, "new_trainer_id": new_trainer_id},
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            trainer = serializer.save(branch=branch)
            return Response(
                BranchTrainerSerializer(trainer).data, status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for new trainer delete (club)
class NewTrainerDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Delete a new trainer from the branch",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Trainer deleted successfully",
                    ),
                },
                example={"message": "Trainer deleted successfully"},
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def delete(self, request, new_trainer_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            trainer = NewTrainer.objects.filter(id=new_trainer_id).first()
            if not trainer:
                return Response(
                    {"error": "New Trainer not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if trainer.branch == branch:
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
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for new trainer edit (club)
class NewTrainerUpdateView(GenericAPIView):
    serializer_class = NewTrainerUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Update the details of a new trainer",
        responses={
            200: NewTrainerSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def patch(self, request, new_trainer_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            trainer = NewTrainer.objects.filter(id=new_trainer_id).first()
            if not trainer:
                return Response(
                    {"error": "New Trainer not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(trainer, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            trainer = serializer.save(branch=branch)
            return Response(
                NewTrainerSerializer(trainer).data, status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch reviews (club)
class BranchReviewsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ReviewsDetailSerializer

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Get all the reviews of the branch",
        responses={
            200: ReviewsDetailSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def get(self, request):
        owner = request.user
        if not owner.is_owner():
            return Response(
                {"error": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        branch = Branch.objects.filter(owner=owner).first()
        if not branch:
            return Response(
                {"error": "Branch does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        reviews = branch.reviews.all()
        if not reviews:
            return Response([], status=status.HTTP_200_OK)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# for branch subscriptions (club)
class BranchSubscriptionsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = SubscriptionSerializer

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Get all the subscriptions of the branch",
        responses={
            200: SubscriptionSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def get(self, request):
        owner = request.user
        if not owner.is_owner():
            return Response(
                {"error": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        branch = Branch.objects.filter(owner=owner).first()
        if not branch:
            return Response(
                {"error": "Branch does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        subscriptions = Subscription.objects.filter(branch=branch)
        if not subscriptions:
            return Response([], status=status.HTTP_200_OK)
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# for branch subscription plans (club)
class BranchSubscriptionPlanDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Delete a subscription plan from the branch",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Subscription plan deleted successfully",
                    ),
                },
                example={"message": "Subscription plan deleted successfully"},
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def delete(self, request, subscription_plan_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            subscription_plan = SubscriptionPlan.objects.filter(
                id=subscription_plan_id
            ).first()
            if not subscription_plan:
                return Response(
                    {"error": "Subscription Plan not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if subscription_plan.subscription.branch == branch:
                subscription_plan.delete()
                return Response(
                    {"message": "Subscription plan deleted successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch subscription add (club)
class BranchSubscriptionAddView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = SubscriptionAddSerializer

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Add a new subscription to the branch",
        responses={
            200: SubscriptionSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            subscriptions = serializer.save(branch=branch)

            return Response(
                SubscriptionSerializer(subscriptions).data,
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# for branch subscription update (club)
class BranchSubscriptionUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = SubscriptionUpdateSerializer

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Update the details of a subscription",
        responses={
            200: SubscriptionSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def put(self, request, subscription_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"}, status=status.HTTP_404_NOT_FOUND
                )
            subscription = Subscription.objects.filter(id=subscription_id).first()
            if not subscription:
                return Response(
                    {"error": "Subscription not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(
                subscription, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            subscription = serializer.save(branch=branch)
            return Response(
                SubscriptionSerializer(subscription).data,
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# for branch subscription delete (club)
class BranchSubscriptionDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Delete a subscription from the branch",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Subscription deleted successfully",
                    ),
                },
                example={"message": "Subscription deleted successfully"},
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def delete(self, request, subscription_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"}, status=status.HTTP_404_NOT_FOUND
                )
            print("subscription_id here", subscription_id)
            subscription = Subscription.objects.filter(id=subscription_id).first()
            print("subscription here", subscription)
            if not subscription:
                print("entered here")
                return Response(
                    {"error": "Subscription not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if subscription.branch == branch:
                print("got me here")
                subscription.delete()
            else:
                return Response(
                    {"error": "Subscription not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                {"message": "Subscription deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# for time delete (club)
class TimeDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Delete a time from the branch",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Time deleted successfully",
                    ),
                },
                example={"message": "Time deleted successfully"},
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def delete(self, request, time_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"}, status=status.HTTP_404_NOT_FOUND
                )
            time = Time.objects.filter(id=time_id).first()
            if not time:
                return Response(
                    {"error": "Time not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if time.day.branch == branch:
                time.delete()
            else:
                return Response(
                    {"error": "Time not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                {"message": "Time deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BranchMembersCountView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Get the number of members in the branch",
        responses={200: BranchMemberSerializer()},
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
    def get(self, request, *args, **kwargs):
        period = self.request.query_params.get("period", "month")
        if period == "week":
            members_count = (
                BranchMember.objects.annotate(date=TruncWeek("created_at"))
                .values("date")
                .annotate(count=Count("id"))
                .order_by("date")
            )
        elif period == "4months":
            members_count = (
                BranchMember.objects.filter(
                    created_at__gte=datetime.now() - relativedelta(months=4)
                )
                .annotate(date=TruncMonth("created_at"))
                .values("date")
                .annotate(count=Count("id"))
                .order_by("date")
            )
        else:
            members_count = (
                BranchMember.objects.annotate(date=TruncMonth("created_at"))
                .values("date")
                .annotate(count=Count("id"))
                .order_by("date")
            )
        return Response(members_count)


# for update branch member from branch (branch)
class MemberSubscriptionUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = MemberSubscriptionUpdateSerializer

    @swagger_auto_schema(
        tags=["clubs"],
        operation_description="Update the details of a branch member",
        request_body=MemberSubscriptionUpdateSerializer,
        responses={
            200: BranchMemberSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def put(self, request, member_subscription_id):
        try:
            owner = request.user
            if not owner.is_owner():
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            print("reached here")
            branch = Branch.objects.filter(owner=owner).first()
            if not branch:
                return Response(
                    {"error": "Branch does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            member_subscription = MemberSubscription.objects.filter(
                id=member_subscription_id
            ).first()
            if not member_subscription:
                return Response(
                    {"error": "Member subscription not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            print("not reached here")
            if not member_subscription.member.branch == branch:
                return Response(
                    {"error": "Branch member not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            print("request.data", request.data)
            serializer = self.get_serializer(
                member_subscription,
                data=request.data,
                partial=True,
            )
            print("reached here Now")
            serializer.is_valid(raise_exception=True)
            print("now here")
            member_subscription = serializer.save()
            print("reached here now")
            return Response(
                MemberSubscriptionSerializerTemp(member_subscription).data,
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


#  ------------------***************------------------  #


#  ------------------- Trainee App -------------------  #


# for branch detail (trainee)
class TraineeBranchDetailView(GenericAPIView):
    serializer_class = TraineeBranchDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the branch details",
        tags=["Trainee App"],
        responses={
            200: TraineeBranchDetailSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def get(self, request, branch_id):
        try:
            branch = Branch.objects.get(id=branch_id)
            serializer = self.get_serializer(branch)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch list (trainee)
class BranchListView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = BranchListSerializer

    @swagger_auto_schema(
        tags=["Trainee App"],
        operation_description="Get all branches",
        responses={
            200: BranchListSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def get(self, request):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_404_FORBIDDEN,
                )
            branches = Branch.objects.all()
            serializer = self.get_serializer(branches, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch member add (trainee)
class BranchMemberJoinView(GenericAPIView):
    serializer_class = BranchMemberJoinSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["Trainee App"],
        operation_description="Join a branch as a member",
        request_body=BranchMemberJoinSerializer(),
        responses={
            200: BranchMemberSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_trainee:
            return Response(
                {"error": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        branch_member = serializer.save()
        return Response(
            BranchMemberSerializer(branch_member).data,
            status=status.HTTP_201_CREATED,
        )


# for branch same country (trainee)
class ClubSameCountryView(GenericAPIView):
    serializer_class = ClubsListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Trainee App"],
        operation_description="Get all clubs that have branches in the user's country",
        responses={200: ClubsListSerializer},
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
    def get(self, request):
        # Get the user's country
        user = request.user
        user_country = user.country

        # Get all branches that have non-empty subscriptions
        branches_with_subscriptions = Branch.objects.filter(
            branch_subscription__isnull=False
        )

        # Get all clubs in the user's country that have these branches
        clubs = Club.objects.filter(
            club_branches__in=branches_with_subscriptions, country=user_country
        )

        serializer = self.serializer_class(clubs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# for branch Nearest to Farthest (trainee)
class ClubNearestToFarthestView(GenericAPIView):
    serializer_class = ClubsListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Trainee App"],
        operation_description="Get all clubs sorted by distance from the user's location",
        responses={200: ClubsListSerializer},
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
    def get(self, request):
        # Get the user's location
        user = request.user
        user_location = user.location

        # Get all branches
        branches = Branch.objects.all()

        # Calculate the distance of each branch from the user's location
        for branch in branches:
            branch.distance = branch.location.distance(user_location)

        # Sort the branches by distance
        branches = sorted(branches, key=lambda x: x.distance)

        # Get all clubs that have these branches and non-empty subscriptions
        clubs = Club.objects.filter(
            club_branches__in=branches, subscriptions__isnull=False
        )

        serializer = self.serializer_class(clubs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# to get all trainers (trainee)
class BranchTrainersView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Trainee App"],
        operation_description="Get all trainers in the branch",
        responses={
            200: BranchTrainerSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def get(self, request):
        try:
            branch_trainers_response = get_branch_trainers(request)
            new_trainers_response = get_new_trainers(request)

            # Combine responses into a single response
            combined_response_data = {
                "trainers": branch_trainers_response.data,
                "new_trainers": new_trainers_response.data,
            }

            return Response(combined_response_data, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for club list (trainee)
class ClubListView(GenericAPIView):
    serializer_class = ClubsListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["Trainee App"],
        operation_description="Get all clubs",
        responses={
            200: ClubsListSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def get(self, request):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"error": "You are not authorized to perform this action"},
                    status=status.HTTP_404_FORBIDDEN,
                )
            clubs = Club.objects.all()
            print("reached here0")
            serializer = self.get_serializer(clubs, many=True)
            print("reached here")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch Ascending order of price (trainee)
class ClubLowestToHighestPricebyView(GenericAPIView):
    serializer_class = ClubsListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Trainee App"],
        operation_description="Get all clubs sorted by the price of their subscriptions in ascending order",
        responses={200: ClubsListSerializer},
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
    def get(self, request):
        # Get the minimum price of all subscriptions
        min_price = Subscription.objects.aggregate(Min("price"))["price__min"]

        # Get all branches that have a subscription with the minimum price
        branches = Branch.objects.filter(branch_subscription__price=min_price)

        # Get all clubs that have these branches
        clubs = Club.objects.filter(club_branches__in=branches)

        serializer = self.serializer_class(clubs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# for member subscription delete (trainee)
class TraineeMemberSubscriptionDeleteView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["Trainee App"],
        operation_description="Delete a member subscription",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Member subscription deleted successfully",
                    ),
                },
                example={"message": "Member subscription deleted successfully"},
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": "Member subscription not found"},
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
    def delete(self, request, member_subscription_id):
        try:
            member_subscription = MemberSubscription.objects.filter(
                id=member_subscription_id
            ).first()
            if not member_subscription:
                return Response(
                    {"error": "Member subscription not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            member_subscription.delete()
            return Response(
                {"message": "Member subscription deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except MemberSubscription.DoesNotExist:
            return Response(
                {"error": "Member subscription not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for branch member update (trainee)
class TraineeBranchMemberUpdateView(GenericAPIView):
    serializer_class = MemberSubscriptionUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["Trainee App"],
        operation_description="Update the details of a branch member",
        request_body=MemberSubscriptionUpdateSerializer,
        responses={
            200: BranchMemberSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, description="Error messages"
                    ),
                },
                example={"error": {"user_type": "This field is required"}},
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
    def put(self, request, member_id):
        user = request.user
        if not user.is_trainee:
            return Response(
                {"error": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        member = BranchMember.objects.get(id=member_id)
        serializer = self.get_serializer(
            member, data=request.data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        branch_member = serializer.save()
        return Response(
            BranchMemberSerializer(branch_member).data,
            status=status.HTTP_200_OK,
        )


# for payment and branch member add (trainee)
class PaymentAndBranchMemberAddView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a payment and add a branch member",
        tags=["Trainee App"],
        operation_id="PaymentAndBranchMemberAddView",
        responses={201: "Created", 400: "Bad Request"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "payment": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        field_name: openapi.Schema(type=openapi.TYPE_STRING)
                        for field_name in PaymentAddSerializer().fields.keys()
                    },
                ),
                "branch_member": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        field_name: openapi.Schema(type=openapi.TYPE_STRING)
                        for field_name in BranchMemberJoinSerializer().fields.keys()
                    },
                ),
            },
        ),
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearertoken>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def post(self, request):
        user = request.user
        if not user.is_trainee:
            return Response(
                {"message": "You are not a trainee"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trainee = Trainee.objects.get(user=user)

        # Add a payment
        payment_serializer = PaymentAddSerializer(
            data=request.data.get("payment"),
            context={"request": request},
        )
        if payment_serializer.is_valid():
            payment = payment_serializer.save(trainee=trainee)
        else:
            return Response(
                payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # Add a branch member
        branch_member_serializer = BranchMemberJoinSerializer(
            data=request.data.get("branch_member"), context={"request": request}
        )
        if branch_member_serializer.is_valid():
            branch_member = branch_member_serializer.save()
        else:
            return Response(
                branch_member_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "payment": PaymentSerializer(payment).data,
                "branch_member": BranchMemberSerializer(branch_member).data,
            },
            status=status.HTTP_201_CREATED,
        )


def get_branch_trainers(request):
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
