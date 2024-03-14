from rest_framework import serializers
from account.serializers import CustomUserSerializer, TraineeSerializer

from .models import (
    Availability,
    Package,
    Program,
    ProgramPlan,
    Review,
    Session,
    Time,
    Trainer,
    Transformations,
    Workout,
    WorkoutFile,
)


class ReviewsDetailSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "trainee",
            "ratings",
            "comment",
            "created_at",
            "updated_at",
        ]


class TransformationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transformations
        fields = [
            "before_picture",
            "after_picture",
            "details",
            "created_at",
            "updated_at",
        ]


class TrainerDetailSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    workouts = serializers.SerializerMethodField()
    programs = serializers.SerializerMethodField()
    trainees = TraineeSerializer(many=True)
    reviews = ReviewsDetailSerializer(many=True)
    transformations = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = [
            "user",
            "slug",
            "bio",
            "sport_field",
            "document_files",
            "id_card",
            "background_image",
            "trainees",
            "number_of_trainees",
            "exp_injuries",
            "physical_disabilities",
            "experience",
            "languages",
            "facebook_url",
            "instagram_url",
            "youtube_url",
            "verified",
            "reviews",
            "workouts",
            "programs",
            "transformations",
            "avg_ratings",
            "number_of_ratings",
        ]

    def get_workouts(self, obj):
        workouts = Workout.objects.filter(trainer=obj)
        return WorkoutListSerializer(workouts, many=True).data

    def get_programs(self, obj):
        programs = Program.objects.filter(trainer=obj)
        return ProgramListSerializer(programs, many=True).data

    def get_transformations(self, obj):
        transformations = Transformations.objects.filter(trainer=obj)
        return TransformationsSerializer(transformations, many=True).data


class TrainerListSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Trainer
        fields = [
            "user",
            "slug",
            "bio",
            "sport_field",
            "background_image",
            "verified",
            "avg_ratings",
            "number_of_ratings",
        ]


class TrainerProgramsSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    programs = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = [
            "user",
            "slug",
            "verified",
            "programs",
        ]

    def get_programs(self, obj):
        programs = Program.objects.filter(trainer=obj)
        return ProgramListSerializer(programs, many=True).data


class TrainerWorkoutsSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    workouts = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = [
            "user",
            "slug",
            "verified",
            "workouts",
        ]

    def get_workouts(self, obj):
        workouts = Workout.objects.filter(trainer=obj)
        return WorkoutListSerializer(workouts, many=True).data


class ProgramPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramPlan
        fields = [
            "id",
            "duration_in_weeks",
            "price",
            "offer_price",
            "max_trainees",
            "created_at",
            "updated_at",
        ]


class ProgramDetailSerializer(serializers.ModelSerializer):
    trainees = TraineeSerializer(many=True)
    reviews = ReviewsDetailSerializer(many=True)
    program_plans = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            "id",
            "title",
            "picture",
            "description",
            "level",
            "method",
            "target_gender",
            "min_age",
            "max_age",
            "program_plans",
            "trainees",
            "current_trainees_count",
            "max_trainees_count",
            "avg_ratings",
            "number_of_ratings",
            "reviews",
            "created_at",
            "updated_at",
        ]

    def get_program_plans(self, obj):
        program_plans = ProgramPlan.objects.filter(program=obj)
        return ProgramPlanSerializer(program_plans, many=True).data


class ProgramListSerializer(serializers.ModelSerializer):

    program_plans = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            "id",
            "title",
            "picture",
            "description",
            "method",
            "current_trainees_count",
            "max_trainees_count",
            "program_plans",
            "avg_ratings",
            "number_of_ratings",
            "created_at",
            "updated_at",
        ]

    def get_program_plans(self, obj):
        program_plans = ProgramPlan.objects.filter(program=obj).first()
        return ProgramPlanSerializer(program_plans).data if program_plans else None


class WorkoutFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutFile
        fields = [
            "file_or_video",
            "title",
            "details",
            "created_at",
            "updated_at",
        ]


class WorkoutDetailSerializer(serializers.ModelSerializer):
    trainees = TraineeSerializer(many=True)
    reviews = ReviewsDetailSerializer(many=True)
    workout_videos_files = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = [
            "id",
            "title",
            "picture",
            "description",
            "level",
            "target_gender",
            "min_age",
            "max_age",
            "price",
            "offer_price",
            "workout_videos_files",
            "number_of_files",
            "current_trainees_count",
            "max_trainees_count",
            "trainees",
            "duration_in_minutes",
            "avg_ratings",
            "number_of_ratings",
            "reviews",
            "created_at",
            "updated_at",
        ]

    def get_workout_videos_files(self, obj):
        workout_videos_files = WorkoutFile.objects.filter(workout=obj)
        return WorkoutFileSerializer(workout_videos_files, many=True).data


class WorkoutListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = [
            "id",
            "title",
            "picture",
            "level",
            "price",
            "offer_price",
            "duration_in_minutes",
            "avg_ratings",
            "number_of_ratings",
            "created_at",
            "updated_at",
        ]


class PackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = [
            "id",
            "session_type",
            "is_active",
            "price",
        ]


class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Time
        fields = [
            "from_time",
            "to_time",
        ]


class AvialabilitySerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    class Meta:
        model = Availability
        fields = [
            "id",
            "day",
            "is_active",
            "time",
        ]

    def get_time(self, obj):
        time = Time.objects.filter(day=obj)
        return TimeSerializer(time, many=True).data


class SessionSerializer(serializers.ModelSerializer):
    package = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = [
            "id",
            "package",
            "duration",
            "target_gender",
            "min_age",
            "max_age",
            "update_body_measure",
            "update_pref_lifestyle",
            "attach_body_img",
            "attach_med_report",
            "availability",
        ]

    def get_package(self, obj):
        package = Package.objects.filter(session=obj)
        print("package", package)
        return PackageSerializer(package, many=True).data

    def get_availability(self, obj):
        try:
            availability = Availability.objects.filter(availablity=obj)
            print("C availability", availability)
            serializer = AvialabilitySerializer(availability, many=True).data
            print("C serializer", serializer)
            return serializer
        except Exception as e:
            print(f"An error occurred while getting availability: {e}")
            return []
