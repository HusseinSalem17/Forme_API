from authentication.models import CustomUser
from authentication.renderers import UserRenderer
from clubs.models import Club, TraineeWishList
from clubs.serializers import (
    ClubDetailSerializer,
    ClubsListSerializer,
    SearchSerializer,
)
from .models import (
    Availability,
    ClientRequest,
    Payment,
    Program,
    ProgramPlan,
    Review,
    Session,
    Time,
    Trainee,
    Transformations,
    Workout,
    Trainer,
    WorkoutFile,
)
from rest_framework.response import Response

from .serializers import (
    AvailabilityUpdateSerializer,
    AvialabilitySerializer,
    ClientRequestAddSerializer,
    ClientRequestTraineeSerializer,
    ClientRequestTrainerSerializer,
    ClientRequestUpdateSerializer,
    JoinProgramPlanSerializer,
    JoinWorkoutSerializer,
    PaymentAddSerializer,
    PaymentSerializer,
    PaymentUpdateSerializer,
    ProgramAddSerializer,
    ProgramListSerializer,
    ProgramPlanAddSerializer,
    ReviewAddSerializer,
    ReviewUpdateSerializer,
    ReviewsDetailSerializer,
    TraineeProgramDetailSerializer,
    TraineeUpdateSerializer,
    TraineeWorkoutDetailSerializer,
    TrainerProgramDetailSerializer,
    ProgramUpdateSerializer,
    SessionSettingsUpdateSerializer,
    SessionSerializer,
    TansformationUpdateSerializer,
    TraineeSerializer,
    TrainerProgramsHomeSerializer,
    TrainerTraineeSerializer,
    TrainerUpdateSerializer,
    TrainerWorkoutsHomeSerializer,
    TrainerWorkoutsListSerializer,
    TransformationAddSerializer,
    TransformationsSerializer,
    WorkoutAddSerializer,
    TrainerWorkoutDetailSerializer,
    TrainerSerializer,
    TrainerListSerializer,
    TrainerProgramsListSerializer,
    WorkoutListSerializer,
    WorkoutUpdateSerializer,
)
from rest_framework import status

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404


from random import shuffle
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.generics import GenericAPIView
from rest_framework import filters


# -----------------Trainee-----------------#

class TraineeUpdateView(GenericAPIView):
    serializer_class = TraineeUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Update a trainee",
        tags=["Trainee App"],
        operation_id="TraineeUpdateView",
        responses={200: TraineeSerializer, 400: "Bad request"},
        security=[{"Bearer": []}],
        request_body=TraineeUpdateSerializer,
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
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainee = Trainee.objects.get(user=user)
            serializer = self.serializer_class(
                trainee, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid():
                trainee = serializer.save()
                return Response(
                    TraineeSerializer(trainee).data, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trainee.DoesNotExist:
            return Response(
                {"message": "Trainee not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TrainerUpdateView(GenericAPIView):
    serializer_class = TrainerUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Update a trainer",
        tags=["Trainer App"],
        operation_id="TrainerUpdateView",
        responses={200: TrainerSerializer, 400: "Bad request"},
        security=[{"Bearer": []}],
        request_body=TrainerUpdateSerializer,
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
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)
            serializer = self.serializer_class(
                trainer, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid():
                trainer = serializer.save()
                return Response(
                    TrainerSerializer(trainer).data, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trainer.DoesNotExist:
            return Response(
                {"message": "Trainer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddProgramToWishlistView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a program to wishlist",
        tags=["Trainee App"],
        operation_id="AddProgramToWishlistView",
        responses={
            201: openapi.Response(
                description="Program added to wishlist successfully.",
                examples={
                    "application/json": {
                        "message": "Program added to wishlist successfully."
                    }
                },
            ),
            400: "Bad request",
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
    def post(self, request, program_id):
        user = request.user
        trainee = Trainee.objects.get(user=user)
        program = get_object_or_404(Program, id=program_id)
        trainee_wishlist, created = TraineeWishList.objects.get_or_create(
            trainee=trainee
        )
        trainee_wishlist.programs_wishlist.add(program)
        trainee_wishlist.save()
        return Response(
            {"message": "Program added to wishlist successfully."},
            status=status.HTTP_201_CREATED,
        )


class RemoveProgramFromWishlistView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Remove a program from wishlist",
        tags=["Trainee App"],
        operation_id="RemoveProgramFromWishlistView",
        responses={
            200: openapi.Response(
                description="Program removed from wishlist successfully.",
                examples={
                    "application/json": {
                        "message": "Program removed from wishlist successfully."
                    }
                },
            ),
            400: "Bad request",
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
    def post(self, request, program_id):
        user = request.user
        trainee = Trainee.objects.get(user=user)
        program = get_object_or_404(Program, id=program_id)
        trainee_wishlist = get_object_or_404(TraineeWishList, trainee=trainee)
        trainee_wishlist.programs_wishlist.remove(program)
        trainee_wishlist.save()
        return Response(
            {"message": "Program removed from wishlist successfully."},
            status=status.HTTP_200_OK,
        )


class AddWorkoutToWishlistView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a workout to wishlist",
        tags=["Trainee App"],
        operation_id="AddWorkoutToWishlistView",
        responses={
            200: openapi.Response(
                description="Workout added to wishlist successfully.",
                examples={
                    "application/json": {
                        "message": "Workout added to wishlist successfully."
                    }
                },
            ),
            400: "Bad request",
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
    def post(self, request, workout_id):
        user = request.user
        trainee = Trainee.objects.get(user=user)
        workout = get_object_or_404(Workout, id=workout_id)
        trainee_wishlist, created = TraineeWishList.objects.get_or_create(
            trainee=trainee
        )
        trainee_wishlist.workouts_wishlist.add(workout)
        trainee_wishlist.save()
        return Response(
            {"message": "Workout added to wishlist successfully."},
            status=status.HTTP_201_CREATED,
        )


class RemoveWorkoutFromWishlistView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Remove a workout from wishlist",
        tags=["Trainee App"],
        operation_id="RemoveProgramFromWishlistView",
        responses={
            200: openapi.Response(
                description="Workout removed from wishlist successfully.",
                examples={
                    "application/json": {
                        "message": "Workout removed from wishlist successfully."
                    }
                },
            ),
            400: "Bad request",
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
    def post(self, request, workout_id):
        user = request.user
        trainee = Trainee.objects.get(user=user)
        workout = get_object_or_404(Workout, id=workout_id)
        trainee_wishlist = get_object_or_404(TraineeWishList, trainee=trainee)
        trainee_wishlist.workouts_wishlist.remove(workout)
        trainee_wishlist.save()
        return Response(
            {"message": "Workout removed from wishlist successfully."},
            status=status.HTTP_200_OK,
        )


class AddTrainerToWishlistView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a trainer to wishlist",
        tags=["Trainee App"],
        operation_id="AddTrainerToWishlistView",
        responses={
            200: openapi.Response(
                description="Trainer added to wishlist successfully.",
                examples={
                    "application/json": {
                        "message": "Trainer added to wishlist successfully."
                    }
                },
            ),
            400: "Bad request",
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
    def post(self, request, trainer_id):
        user = request.user
        trainee = Trainee.objects.get(user=user)
        trainer = get_object_or_404(Trainer, id=trainer_id)
        trainee_wishlist, created = TraineeWishList.objects.get_or_create(
            trainee=trainee
        )
        trainee_wishlist.trainers_wishlist.add(trainer)
        trainee_wishlist.save()
        return Response(
            {"message": "Trainer added to wishlist successfully."},
            status=status.HTTP_201_CREATED,
        )


class RemoveTrainerFromWishlistView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Remove a trainer from wishlist",
        tags=["Trainee App"],
        operation_id="RemoveProgramFromWishlistView",
        responses={
            200: openapi.Response(
                description="Program removed from wishlist successfully.",
                examples={
                    "application/json": {
                        "message": "Program removed from wishlist successfully."
                    }
                },
            ),
            400: "Bad request",
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
    def post(self, request, trainer_id):
        user = request.user
        trainee = Trainee.objects.get(user=user)
        trainer = get_object_or_404(Trainer, id=trainer_id)
        trainee_wishlist = get_object_or_404(TraineeWishList, trainee=trainee)
        trainee_wishlist.trainers_wishlist.remove(trainer)
        trainee_wishlist.save()
        return Response(
            {"message": "Trainer removed from wishlist successfully."},
            status=status.HTTP_200_OK,
        )


class AddClubToWishlistView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a club to wishlist",
        tags=["Trainee App"],
        operation_id="AddClubToWishlistView",
        responses={
            200: openapi.Response(
                description="Club added to wishlist successfully.",
                examples={
                    "application/json": {
                        "message": "Club added to wishlist successfully."
                    }
                },
            ),
            400: "Bad request",
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
    def post(self, request, club_id):
        user = request.user
        trainee = Trainee.objects.get(user=user)
        club = get_object_or_404(Club, id=club_id)
        trainee_wishlist, created = TraineeWishList.objects.get_or_create(
            trainee=trainee
        )
        trainee_wishlist.clubs_wishlist.add(club)
        trainee_wishlist.save()
        return Response(
            {"message": "Club added to wishlist successfully."},
            status=status.HTTP_201_CREATED,
        )


class RemoveClubFromWishlistView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Remove a club from wishlist",
        tags=["Trainee App"],
        operation_id="RemoveProgramFromWishlistView",
        responses={
            200: openapi.Response(
                description="Program removed from wishlist successfully.",
                examples={
                    "application/json": {
                        "message": "Program removed from wishlist successfully."
                    }
                },
            ),
            400: "Bad request",
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
    def post(self, request, club_id):
        user = request.user
        trainee = Trainee.objects.get(user=user)
        club = get_object_or_404(Club, id=club_id)
        trainee_wishlist = get_object_or_404(TraineeWishList, trainee=trainee)
        trainee_wishlist.clubs_wishlist.remove(club)
        trainee_wishlist.save()
        return Response(
            {"message": "Club removed from wishlist successfully."},
            status=status.HTTP_200_OK,
        )


# for clinet request (trainee)
class ClientRequestTraineeView(GenericAPIView):

    serializer_class = ClientRequestTraineeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a list of client requests for Trainee",
        tags=["Trainee App"],
        operation_id="ClientRequestTraineeView",
        responses={200: ClientRequestTraineeSerializer(many=True)},
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
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainee = Trainee.objects.get(user=user)
            client_requests = ClientRequest.objects.filter(trainee=trainee)
            serializer = self.serializer_class(client_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Trainee.DoesNotExist:
            return Response(
                {"message": "Trainee not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HomeView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a list of trainers with their programs, workouts, and top-rated trainers for Home Screen",
        tags=["Trainee App"],
        operation_id="HomeView",
        responses={200: "OK", 400: "Bad Request"},
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
        if not user.is_trainee:
            return Response(
                {"message": "You are not a trainee"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trainee = Trainee.objects.get(user=user)

        # Get trainers with their programs
        program_trainers = list(
            Trainer.objects.filter(trainer_programs__isnull=False).distinct()
        )
        shuffle(program_trainers)
        program_trainers_data = TrainerProgramsHomeSerializer(
            program_trainers, many=True
        ).data

        # Get trainers with their workouts
        workout_trainers = list(
            Trainer.objects.filter(trainer_workouts__isnull=False).distinct()
        )
        shuffle(workout_trainers)
        workout_trainers_data = TrainerWorkoutsHomeSerializer(
            workout_trainers, many=True
        ).data

        # Get top-rated trainers
        top_trainers = list(Trainer.objects.order_by("-avg_ratings")[:10])
        shuffle(top_trainers)
        top_trainers_data = TrainerListSerializer(top_trainers, many=True).data

        return Response(
            {
                "program_trainers": program_trainers_data,
                "workout_trainers": workout_trainers_data,
                "top_trainers": top_trainers_data,
            },
            status=status.HTTP_200_OK,
        )


# for client request add(trainee)
class ClientRequestAddView(GenericAPIView):

    serializer_class = ClientRequestAddSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a client request",
        tags=["Trainee App"],
        operation_id="ClientRequestAddView",
        responses={
            200: ClientRequestTraineeSerializer,
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
        request_body=ClientRequestAddSerializer,
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
    def post(self, request):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                print("reached here 0")
                client_request = serializer.save()
                return Response(
                    ClientRequestTraineeSerializer(client_request).data,
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for client request update(trainee, trainer)
class ClientRequestUpdateView(GenericAPIView):

    serializer_class = ClientRequestUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Update a client request",
        tags=["Trainer App", "Trainee App"],
        operation_id="ClientRequestUpdateView",
        responses={
            200: ClientRequestTraineeSerializer,
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
        request_body=ClientRequestUpdateSerializer,
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
    def patch(self, request, client_request_id):
        try:
            user = request.user
            client_request = ClientRequest.objects.get(pk=client_request_id)
            print("reached here 0")
            serializer = self.serializer_class(
                client_request,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            if serializer.is_valid():
                client_request = serializer.save()
                return Response(
                    ClientRequestTraineeSerializer(client_request).data,
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ClientRequest.DoesNotExist:
            return Response(
                {"message": "Client request not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for client request (trainer)
class ClientRequestTrainerView(GenericAPIView):

    serializer_class = ClientRequestTrainerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a list of client requests for Trainer",
        tags=["Trainer App"],
        operation_id="TrainerClientRequestView",
        responses={
            200: ClientRequestTrainerSerializer(many=True),
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
    def get(self, request):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)
            programs = Program.objects.filter(trainer=trainer)
            program_plans = ProgramPlan.objects.filter(program__in=programs)
            client_requests = ClientRequest.objects.filter(
                program_plan__in=program_plans
            )
            serializer = self.serializer_class(client_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Trainer.DoesNotExist:
            return Response(
                {"message": "Trainer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for review add (trainee)
class ReviewAddView(GenericAPIView):

    serializer_class = ReviewAddSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a review",
        tags=["Trainee App"],
        operation_id="ReviewAddView",
        responses={
            201: ReviewsDetailSerializer,
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
                            "user_type": ["User type is required."],
                            "rating": ["Rating is required."],
                        }
                    },
                ),
            ),
        },
        security=[{"Bearer": []}],
        request_body=ReviewAddSerializer,
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
    def post(self, request):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                review = serializer.save()
                return Response(
                    ReviewsDetailSerializer(review).data, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for review update (trainee)
class ReviewUpdateView(GenericAPIView):

    serializer_class = ReviewUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, review_id=None):
        try:
            return Review.objects.get(pk=review_id)
        except Transformations.DoesNotExist:
            raise Response(
                {"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Update a review",
        tags=["Trainee App"],
        operation_id="ReviewUpdateView",
        responses={
            200: ReviewsDetailSerializer,
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
                            "user_type": ["User type is required."],
                            "rating": ["Rating is required."],
                        }
                    },
                ),
            ),
        },
        security=[{"Bearer": []}],
        request_body=ReviewUpdateSerializer,
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
    def patch(self, request, review_id):
        try:
            user = request.user
            review = self.get_object(review_id)
            serializer = self.serializer_class(review, data=request.data, partial=True)
            if serializer.is_valid():
                review = serializer.save()
                return Response(
                    ReviewsDetailSerializer(review).data, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReviewDeleteView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, review_id):
        try:
            return Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            raise Response(
                {"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Delete a review",
        tags=["Trainee App"],
        operation_id="ReviewDeleteView",
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
                        "message": "Review deleted successfully",
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
                            "user_type": ["User type is required."],
                            "rating": ["Rating is required."],
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
    def delete(self, request, review_id):
        try:
            user = request.user
            trainee = Trainee.objects.get(user=user)
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not Review.objects.filter(pk=review_id, trainee=trainee).exists():
                return Response(
                    {"message": "Review is not for this Trainee"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            review = self.get_object(review_id)
            review.delete()
            return Response(
                {"message": "Review deleted successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for availability screen (trainer)
class AvailabilityUpdateView(GenericAPIView):

    serializer_class = AvailabilityUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Update availability",
        responses={
            200: AvialabilitySerializer,
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
        tags=["Trainer App"],
        operation_id="AvailabilityUpdateView",
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
        request_body=AvailabilityUpdateSerializer,
    )
    def put(self, request, availability_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)
            session = Session.objects.filter(trainer=trainer).first()
            if not Availability.objects.filter(session=session).exists():
                return Response(
                    {"message": "Time is not for this Trainer"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            availability = Availability.objects.get(pk=availability_id)
            serializer = self.serializer_class(availability, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    AvialabilitySerializer(availability).data, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for home screen (trainee)
class ProgramsTrainersHomeView(GenericAPIView):

    serializer_class = TrainerProgramsHomeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a list of trainers with their programs for Home Screen",
        tags=["Trainee App"],
        operation_id="ProgramsTrainersHomeView",
        responses={
            200: TrainerProgramsHomeSerializer(many=True),
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
    def get(self, request):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainers = list(
                Trainer.objects.filter(trainer_programs__isnull=False).distinct()
            )
            if not trainers:
                return Response(
                    {"error": "No trainers found"}, status=status.HTTP_404_NOT_FOUND
                )
            shuffle(trainers)
            return Response(
                self.serializer_class(trainers, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# for home screen (trainee)
class ProgramsTrainerListView(GenericAPIView):

    serializer_class = TrainerProgramsListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a list of trainers with their programs for see more programs screen",
        tags=["Trainee App"],
        operation_id="ProgramsTrainerListView",
        responses={
            200: TrainerProgramsListSerializer(many=True),
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
    def get(self, request):
        try:
            trainers = Trainer.objects.all()
            if not trainers:
                return Response(
                    {"message": "No trainers found"}, status=status.HTTP_404_NOT_FOUND
                )
            shuffle(list(trainers))
            return Response(
                self.serializer_class(trainers, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for program detail (trainee)
class TraineeProgramsDetailView(GenericAPIView):

    serializer_class = TraineeProgramDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a program details by program id",
        tags=["Trainee App"],
        operation_id="TraineeProgramsDetailView",
        responses={
            200: TraineeProgramDetailSerializer,
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
    def get(self, request, program_id):
        try:
            program = Program.objects.get(pk=program_id)
            return Response(
                self.serializer_class(program).data, status=status.HTTP_200_OK
            )
        except Program.DoesNotExist:
            return Response(
                {"message": "Program not found"}, status=status.HTTP_404_NOT_FOUND
            )


# for program detail (trainer)
class TrainerProgramsDetailView(GenericAPIView):

    serializer_class = TrainerProgramDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a program details by program id",
        tags=["Trainer App"],
        operation_id="TrainerProgramsDetailView",
        responses={
            200: TrainerProgramDetailSerializer,
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
    def get(self, request, program_id):
        try:
            program = Program.objects.get(pk=program_id)
            return Response(
                self.serializer_class(program).data, status=status.HTTP_200_OK
            )
        except Program.DoesNotExist:
            return Response(
                {"message": "Program not found"}, status=status.HTTP_404_NOT_FOUND
            )


# for add program (trainer)
class ProgramAddView(GenericAPIView):

    serializer_class = ProgramAddSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a program",
        tags=["Trainer App"],
        operation_id="ProgramsAddView",
        responses={
            201: TrainerProgramDetailSerializer,
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
        request_body=ProgramAddSerializer,
    )
    def post(self, request):
        user = request.user
        if not user.is_trainer:
            return Response(
                {"message": "You are not a trainer."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trainer = Trainer.objects.get(user=user)

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            program = serializer.save(trainer=trainer)
            return Response(
                TrainerProgramDetailSerializer(program).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for add program plan (trainer)
class ProgramPlanAddView(GenericAPIView):

    serializer_class = ProgramPlanAddSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a program plan",
        tags=["Trainer App"],
        responses={
            201: TrainerProgramDetailSerializer,
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
        request_body=ProgramPlanAddSerializer,
    )
    def post(self, request, program_id):
        user = request.user
        if not user.is_trainer:
            return Response(
                {"message": "You are not a trainer."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trainer = Trainer.objects.get(user=user)
        if not Program.objects.filter(trainer=trainer).exists():
            return Response(
                {"message": "Program is not for this Trainer"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not Program.objects.filter(trainer=trainer).exists():
            return Response(
                {"message": "Program is not for this Trainer"},
                status=status.HTTP_404_NOT_FOUND,
            )
        program = Program.objects.get(id=program_id)
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            program_plan = serializer.save(program=program)
            return Response(
                TrainerProgramDetailSerializer(program_plan.program).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for join program (trainee) (not yet)
class ProgramTraineeJoinView(GenericAPIView):
    serializer_class = JoinProgramPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Join a program",
        tags=["Trainee App"],
        responses={
            201: TraineeProgramDetailSerializer,
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
        request_body=JoinProgramPlanSerializer,
    )
    def post(self, request):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                program = serializer.save()
                return Response(
                    TraineeProgramDetailSerializer(program).data,
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Program.DoesNotExist:
            return Response(
                {"message": "Program not found"}, status=status.HTTP_404_NOT_FOUND
            )


# for update program (trainer)
class ProgramUpdateView(GenericAPIView):

    serializer_class = ProgramUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, program_id):
        try:
            return Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            raise Response(
                {"message": "Yor are not a trainer."}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Update a program",
        tags=["Trainer App"],
        responses={200: TrainerProgramDetailSerializer, 400: "Bad request"},
        security=[{"Bearer": []}],
        operation_id="ProgramUpdateView",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        request_body=ProgramUpdateSerializer,
    )
    def put(self, request, program_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)

            if not Program.objects.filter(trainer=trainer).exists():
                return Response(
                    {"message": "Program is not for this Trainer"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            program = self.get_object(program_id)
            serializer = self.serializer_class(program, data=request.data, partial=True)
            if serializer.is_valid():
                program = serializer.save()
                return Response(
                    TrainerProgramDetailSerializer(program).data,
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for delete program (trainer)
class ProgramDeleteView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, program_id):
        try:
            return Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            raise Response(
                {"message": "Program not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Delete a program",
        tags=["Trainer App"],
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
        security=[{"Bearer": []}],
        operation_id="ProgramDeleteView",
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
    def delete(self, request, program_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)

            if not Program.objects.filter(trainer=trainer).exists():
                return Response(
                    {"message": "Program is not for this Trainer"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            program = self.get_object(program_id)
            program.delete()
            return Response(
                {"message": "Program deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# for session settings (trainer)
class SessionSettingsUpdateView(GenericAPIView):

    serializer_class = SessionSettingsUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Update session settings",
        tags=["Trainer App"],
        operation_id="SessionSettingsUpdateView",
        responses={
            200: SessionSerializer,
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
        request_body=SessionSettingsUpdateSerializer,
    )
    def put(self, request):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)
            session = Session.objects.filter(trainer=trainer).first()
            if session:
                serializer = self.serializer_class(session, data=request.data)
                if serializer.is_valid():
                    session = serializer.save()

                    return Response(
                        SessionSerializer(session).data, status=status.HTTP_200_OK
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Trainer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# for time of days (trainer)
class TimeDeleteView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, time_id):
        try:
            return Time.objects.get(pk=time_id)
        except Time.DoesNotExist:
            raise Response(
                {"message": "Time not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Delete a time",
        tags=["Trainer App"],
        operation_id="TimeDeleteView",
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
                        "message": "Time deleted successfully",
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
    def delete(self, request, time_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Time.objects.filter(id=time_id).exists():
                time = self.get_object(time_id)
                time.delete()
                return Response(
                    {"message": "Time deleted successfully"},
                    status=status.HTTP_200,
                )
            return Response(
                {"message": "Time not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for trainer detail (trainee) 1
class TraineeTrainerDetailView(GenericAPIView):

    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a trainer details by user id",
        tags=["Trainee App"],
        operation_id="TraineeTrainerDetailView",
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
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            trainer = get_object_or_404(Trainer, user=user)
            if not trainer:
                return Response(
                    {"message": "Trainer not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(trainer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for trainer detail (trainer) 2
class TrainerDetailView(GenericAPIView):

    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a trainer details by user id",
        tags=["Trainer App"],
        operation_id="TrainerDetailView",
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
    def get(self, request):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = get_object_or_404(Trainer, user=user)
            serializer = self.serializer_class(trainer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Trainer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# to get trainee details (trainee) 1
class TraineeDetailView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get Trainee Details for Trainee",
        tags=["Trainee App"],
        operation_id="get_trainee_detail",
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
    def get(self, request):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not Trainee.objects.filter(user=user).exists():
                print("not trainee2")
                return Response(
                    {"message": "Trainee not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            trainee = Trainee.objects.get(user=user)
            serializer = TraineeSerializer(trainee)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# to get trainee details (trainer) 2
class TrainerTraineeDetailView(GenericAPIView):
    serializer_class = TrainerTraineeSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get Trainee Details for Trainee",
        tags=["Trainer App"],
        operation_id="get_trainer_trainee_detail",
        responses={
            200: TrainerTraineeSerializer,
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
    def get(self, request, trainee_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = CustomUser.objects.get(id=trainee_id)
            if not Trainee.objects.filter(user=user).exists():
                return Response(
                    {"message": "Trainee not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            trainee = Trainee.objects.get(user=user)
            serializer = self.serializer_class(trainee)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# to get top trainer (trainee)
class TopRatedTrainersView(GenericAPIView):

    serializer_class = TrainerListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a list of top rated trainers for Home Screen",
        tags=["Trainee App"],
        operation_id="TopRatedTrainersHomeView",
        responses={
            200: TrainerListSerializer(many=True),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Message"
                        ),
                    },
                    example={"message": "No trainers found"},
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
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainers = list(Trainer.objects.order_by("-avg_ratings")[:10])
            if not trainers:
                return Response(
                    {"message": "No trainers found"}, status=status.HTTP_404_NOT_FOUND
                )
            shuffle(trainers)
            serializer = self.get_serializer(trainers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# to get list of trainers (trainee)
class TrainerListView(GenericAPIView):

    serializer_class = TrainerListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a list of trainers for See more trainers screen",
        tags=["Trainee App"],
        operation_id="TrainerListView",
        responses={
            200: TrainerListSerializer(many=True),
            400: openapi.Response(
                "Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Message"
                        ),
                    },
                    example={"message": "No trainers found"},
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
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainers = Trainer.objects.all()
            if not trainers:
                return Response(
                    {"message": "No trainers found"}, status=status.HTTP_404_NOT_FOUND
                )
            shuffle(list(trainers))
            serializer = self.serializer_class(trainers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# to get workouts home (trainee)
class WorkoutsTrainersHomeView(GenericAPIView):

    serializer_class = TrainerWorkoutsHomeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a list of trainers with their workouts for Home Screen",
        tags=["Trainee App"],
        operation_id="WorkoutsTrainersView",
        responses={200: TrainerWorkoutsHomeSerializer(many=True)},
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
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainers = list(
                Trainer.objects.filter(trainer_workouts__isnull=False).distinct()
            )
            if not trainers:
                return Response(
                    {"message": "No trainers found"}, status=status.HTTP_404_NOT_FOUND
                )
            shuffle(trainers)
            return Response(
                self.serializer_class(trainers, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# to get workouts list (trainee)
class WorkoutsTrainerListView(GenericAPIView):

    serializer_class = TrainerWorkoutsListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a list of trainers with their workouts for see more workouts screen",
        tags=["Trainee App"],
        operation_id="WorkoutsTrainerListView",
        responses={
            200: TrainerWorkoutsListSerializer(many=True),
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
    def get(self, request):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainers = list(
                Trainer.objects.filter(trainer_workouts__isnull=False).distinct()
            )
            if not trainers:
                return Response(
                    {"message": "No trainers found"}, status=status.HTTP_404_NOT_FOUND
                )
            shuffle(list(trainers))
            return Response(
                self.serializer_class(trainers, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# to join workout (trainee)
class WorkoutTraineeJoinView(GenericAPIView):
    serializer_class = JoinWorkoutSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, workout_id):
        try:
            return Workout.objects.get(pk=workout_id)
        except Workout.DoesNotExist:
            raise Response(
                {"message": "Workout not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Join a workout",
        tags=["Trainee App"],
        operation_id="WorkoutTraineeJoinView",
        responses={
            200: TraineeWorkoutDetailSerializer,
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
        request_body=JoinWorkoutSerializer,
    )
    def patch(self, request, workout_id):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            workout = self.get_object(workout_id)
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                workout = serializer.save()
                return Response(
                    TraineeWorkoutDetailSerializer(workout).data,
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentAndWorkoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a payment and join a workout",
        tags=["Trainee App"],
        operation_id="PaymentAndWorkoutView",
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
                "workout": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        field_name: openapi.Schema(type=openapi.TYPE_STRING)
                        for field_name in JoinWorkoutSerializer().fields.keys()
                    },
                ),
            },
        ),
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

        # Join a workout
        workout_serializer = JoinWorkoutSerializer(
            data=request.data.get("workout"), context={"request": request}
        )
        if workout_serializer.is_valid():
            workout = workout_serializer.save()
        else:
            return Response(
                workout_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "payment": PaymentSerializer(payment).data,
                "workout": TraineeWorkoutDetailSerializer(workout).data,
            },
            status=status.HTTP_201_CREATED,
        )


# for workout detail (trainee)
class TraineeWorkoutDetailView(GenericAPIView):

    serializer_class = TraineeWorkoutDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a workout details by workout id",
        tags=["Trainee App"],
        operation_id="TraineeWorkoutDetailView",
        responses={
            200: TraineeWorkoutDetailSerializer,
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
    def get(self, request, workout_id):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            workout = Workout.objects.get(pk=workout_id)
            return Response(
                self.serializer_class(workout).data, status=status.HTTP_200_OK
            )
        except Workout.DoesNotExist:
            return Response(
                {"message": "Workout not found"}, status=status.HTTP_404_NOT_FOUND
            )


# for workout detail (trainer)
class TrainerWorkoutDetailView(GenericAPIView):

    serializer_class = TrainerWorkoutDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get a workout details by workout id",
        tags=["Trainer App"],
        operation_id="TrainerWorkoutDetailView",
        responses={
            200: TrainerWorkoutDetailSerializer,
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
    def get(self, request, workout_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            workout = Workout.objects.get(pk=workout_id)
            return Response(
                self.serializer_class(workout).data, status=status.HTTP_200_OK
            )
        except Workout.DoesNotExist:
            return Response(
                {"message": "Workout not found"}, status=status.HTTP_404_NOT_FOUND
            )


# for workout add (trainer)
class WorkoutAddView(GenericAPIView):

    serializer_class = WorkoutAddSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a workout",
        tags=["Trainer App"],
        operation_id="WorkoutAddView",
        responses={
            201: TrainerWorkoutDetailSerializer,
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "picture": openapi.Schema(type=openapi.TYPE_FILE),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "level": openapi.Schema(type=openapi.TYPE_STRING),
                "target_gender": openapi.Schema(type=openapi.TYPE_STRING),
                "price": openapi.Schema(type=openapi.TYPE_INTEGER),
                "min_age": openapi.Schema(type=openapi.TYPE_INTEGER),
                "max_age": openapi.Schema(type=openapi.TYPE_INTEGER),
                "is_offer": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "sport_field": openapi.Schema(type=openapi.TYPE_STRING),
                "offer_price": openapi.Schema(type=openapi.TYPE_INTEGER),
                "workout_files": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "file_or_video": openapi.Schema(type=openapi.TYPE_FILE),
                            "title": openapi.Schema(type=openapi.TYPE_STRING),
                            "details": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                ),
            },
            required=[
                "title",
                "sport_field",
                "description",
                "level",
                "price",
            ],
        ),
    )
    def post(self, request):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                workout = serializer.save(trainer=trainer)
                return Response(
                    TrainerWorkoutDetailSerializer(workout).data,
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trainer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for workout update (trainer)
class WorkoutUpdateView(GenericAPIView):

    serializer_class = WorkoutUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, workout_id):
        try:
            return Workout.objects.get(pk=workout_id)
        except Workout.DoesNotExist:
            raise Response(
                {"message": "Workout not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="update a workout",
        tags=["Trainer App"],
        operation_id="WorkoutUpdateView",
        responses={
            200: TrainerWorkoutDetailSerializer,
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
        request_body=WorkoutUpdateSerializer,
    )
    def put(self, request, workout_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)

            if not Workout.objects.filter(trainer=trainer).exists():
                return Response(
                    {"message": "Workout is not for this Trainer"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            workout = self.get_object(workout_id)
            serializer = self.serializer_class(workout, data=request.data, partial=True)
            if serializer.is_valid():
                workout = serializer.save()
                return Response(
                    TrainerWorkoutDetailSerializer(workout).data,
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# for workout delete (trainer)
class WorkoutDeleteView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, workout_id):
        try:
            return Workout.objects.get(pk=workout_id)
        except Workout.DoesNotExist:
            raise Response(
                {"message": "Workout not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Delete a workout",
        tags=["Trainer App"],
        operation_id="WorkoutDeleteView",
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
    def delete(self, request, workout_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)

            if not Workout.objects.filter(trainer=trainer).exists():
                return Response(
                    {"message": "Workout is not for this Trainer"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            workout = self.get_object(workout_id)
            workout.delete()
            return Response(
                {"message": "Workout deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for workout file delete (trainer)
class WorkoutFileDeleteView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, workout_file_id):
        try:
            return WorkoutFile.objects.get(pk=workout_file_id)
        except WorkoutFile.DoesNotExist:
            raise Response(
                {"message": "Workout file not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Delete a workout file",
        tags=["Trainer App"],
        operation_id="WorkoutFileDeleteView",
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
                        "message": "Workout file deleted successfully",
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
    def delete(self, request, workout_file_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)

            if not WorkoutFile.objects.filter(workout__trainer=trainer).exists():
                return Response(
                    {"message": "Workout file is not for this Trainer"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            workout_file = self.get_object(workout_file_id)
            workout_file.delete()
            return Response(
                {"message": "Workout file deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"message": "An error occurred while deleting the workout file."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# for transformation add (trainer)
class TransformationsAddView(GenericAPIView):

    serializer_class = TransformationAddSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a transformation",
        tags=["Trainer App"],
        security=[{"Bearer": []}],
        responses={
            201: TransformationsSerializer,
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
        operation_id="TransformationsAddView",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        request_body=TransformationAddSerializer,
    )
    def post(self, request):

        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainee = Trainee.objects.get(user=user)
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                t = serializer.save(trainee=trainee)
                return Response(
                    TransformationsSerializer(t).data, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trainee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for transformation update (trainer)
class TransformationUpdateView(GenericAPIView):

    serializer_class = TansformationUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, transformation_id):
        try:
            return Transformations.objects.get(pk=transformation_id)
        except Transformations.DoesNotExist:
            raise Response(
                {"message": "Transformation not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update a transformation",
        tags=["Trainer App"],
        operation_id="TransforamtionsUpdateView",
        responses={
            201: TransformationsSerializer,
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
        request_body=TansformationUpdateSerializer,
    )
    def patch(self, request, transformation_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)
            if not Transformations.objects.filter(trainer=trainer).exists():
                return Response(
                    {"message": "Transformation is not for this Trainer"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            transformation = self.get_object(transformation_id)
            serializer = self.serializer_class(
                transformation, data=request.data, partial=True
            )
            if serializer.is_valid():
                t = serializer.save()
                return Response(
                    TransformationsSerializer(t).data, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# for transformation delete (trainer)
class TransformationDeleteView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, transformation_id):
        try:
            return Transformations.objects.get(pk=transformation_id)
        except Transformations.DoesNotExist:
            raise Response(
                {"message": "Transformation not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Delete a transformation",
        tags=["Trainer App"],
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
                        "message": "Transformation deleted successfully",
                    },
                ),
            ),
            404: openapi.Response(
                "Not Found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Error message"
                        ),
                    },
                    example={
                        "message": "Transformation not found",
                    },
                ),
            ),
        },
        security=[{"Bearer": []}],
        operation_id="TransformationsDeleteView",
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
    def delete(self, request, transformation_id):
        try:
            user = request.user
            if not user.is_trainer:
                return Response(
                    {"message": "You are not a trainer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainer = Trainer.objects.get(user=user)

            if not Transformations.objects.filter(trainer=trainer).exists():
                return Response(
                    {"message": "Transformation is not for this Trainer"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            transformation = self.get_object(transformation_id)
            transformation.delete()
            return Response(
                {"message": "Transformation deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# for add payment (Payment)
class PaymentAddView(GenericAPIView):

    serializer_class = PaymentAddSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a payment",
        tags=["Payment Operations"],
        operation_id="PaymentAddView",
        responses={
            201: PaymentSerializer,
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
        request_body=PaymentAddSerializer,
    )
    def post(self, request):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainee = Trainee.objects.get(user=user)
            serializer = self.serializer_class(
                data=request.data,
                context={
                    "request": request,
                },
            )
            if serializer.is_valid():
                payment = serializer.save(trainee=trainee)
                return Response(
                    PaymentSerializer(payment).data, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trainee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentAndProgramView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Add a payment and join a program",
        tags=["Trainee App"],
        operation_id="PaymentAndProgramView",
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
                "program": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        field_name: openapi.Schema(type=openapi.TYPE_STRING)
                        for field_name in JoinProgramPlanSerializer().fields.keys()
                    },
                ),
            },
        ),
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

        # Join a program
        program_serializer = JoinProgramPlanSerializer(
            data=request.data.get("program"), context={"request": request}
        )
        if program_serializer.is_valid():
            program = program_serializer.save()
        else:
            return Response(
                program_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "payment": PaymentSerializer(payment).data,
                "program": TraineeProgramDetailSerializer(program).data,
            },
            status=status.HTTP_201_CREATED,
        )


# for update payment (Payment)
class PaymentUpdateView(GenericAPIView):

    serializer_class = PaymentUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, payment_id):
        try:
            return Payment.objects.get(pk=payment_id)
        except Payment.DoesNotExist:
            raise Response(
                {"message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_description="Update a payment",
        tags=["Payment Operations"],
        operation_id="PaymentUpdateView",
        responses={
            200: PaymentSerializer,
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
        request_body=PaymentUpdateSerializer,
    )
    def patch(self, request, payment_id=None):
        try:
            user = request.user
            if not user.is_trainee:
                return Response(
                    {"message": "You are not a trainee"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trainee = Trainee.objects.get(user=user)
            payment = Payment.objects.get(pk=payment_id, trainee=trainee)
            serializer = self.serializer_class(
                payment,
                data=request.data,
                context={"request": request},
                partial=True,
            )
            if serializer.is_valid():
                payment = serializer.save()
                return Response(
                    PaymentSerializer(payment).data, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trainee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SearchView(APIView):

    @swagger_auto_schema(
        operation_description="Search for programs and workouts and trainers and clubs by query",
        tags=["Trainee App"],
        operation_id="SearchView",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "programs": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "title": openapi.Schema(type=openapi.TYPE_STRING),
                                "description": openapi.Schema(type=openapi.TYPE_STRING),
                                "level": openapi.Schema(type=openapi.TYPE_STRING),
                                "type": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    ),
                    "workouts": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "title": openapi.Schema(type=openapi.TYPE_STRING),
                                "description": openapi.Schema(type=openapi.TYPE_STRING),
                                "level": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    ),
                },
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
            openapi.Parameter(
                "q",
                openapi.IN_QUERY,
                description="Search query",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
    )
    def get(self, request):
        query = request.query_params.get("q", "")

        # Search in Programs
        program_queryset = Program.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(level__icontains=query)
            | Q(type__icontains=query)
        )
        program_serializer = ProgramListSerializer(program_queryset, many=True)

        # Search in Workouts
        workout_queryset = Workout.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(level__icontains=query)
        )
        workout_serializer = WorkoutListSerializer(workout_queryset, many=True)

        # Search in Trainers
        trainer_queryset = Trainer.objects.filter(
            Q(user__username__icontains=query)
            | Q(bio__icontains=query)
            | Q(sport_field__icontains=query)
        )
        trainer_serializer = TrainerListSerializer(trainer_queryset, many=True)

        # Search in Clubs
        club_queryset = Club.objects.filter(
            Q(property_name__icontains=query)
            | Q(club_website__icontains=query)
            | Q(club_registration_number__icontains=query)
            | Q(sport_field__icontains=query)
        )
        club_serializer = ClubsListSerializer(club_queryset, many=True)
        return Response(
            {
                "programs": program_serializer.data,
                "workouts": workout_serializer.data,
                "trainers": trainer_serializer.data,
                "clubs": club_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
