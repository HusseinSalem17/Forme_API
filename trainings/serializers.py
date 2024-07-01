from rest_framework import serializers

from authentication.serializers import CustomUserSerializer, CustomUserUpdateSerializer
from clubs.models import Club, TraineeWishList

from .models import (
    Availability,
    ClientRequest,
    Document,
    Package,
    Payment,
    Program,
    ProgramPlan,
    Review,
    Session,
    Time,
    Trainee,
    Trainer,
    Transformations,
    Workout,
    WorkoutFile,
)

from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from django.conf import settings


class WorkoutListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

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


class TrainerTraineeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Trainee
        fields = [
            "user",
            "fitness_goals",
            "current_physical_level",
        ]


class TrainerTraineeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Trainee
        fields = [
            "user",
            "fitness_goals",
            "current_physical_level",
        ]


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


class TrainerProgramsHomeSerializer(serializers.ModelSerializer):
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
        programs = Program.objects.filter(trainer=obj).first()
        if not programs:
            return None
        return ProgramListSerializer(programs).data if programs else None


class TrainerProgramsListSerializer(serializers.ModelSerializer):
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
        if not programs:
            return None
        return ProgramListSerializer(programs, many=True).data


class TrainerWorkoutsHomeSerializer(serializers.ModelSerializer):
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
        workout = Workout.objects.filter(trainer=obj).first()
        if not workout:
            return None
        return WorkoutListSerializer(workout).data if workout else None


class TrainerWorkoutsListSerializer(serializers.ModelSerializer):
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
        if not workouts:
            return None
        return WorkoutListSerializer(workouts, many=True).data


class ReviewsDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "ratings",
            "comment",
            "created_at",
            "updated_at",
        ]


class TraineeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    programs = serializers.SerializerMethodField()
    workouts = serializers.SerializerMethodField()
    # reviews = ReviewsDetailSerializer(many=True)

    class Meta:
        model = Trainee
        fields = [
            "user",
            "fitness_goals",
            "current_physical_level",
            "programs",
            "workouts",
            # "reviews",
        ]

    def get_programs(self, obj):
        programs = Program.objects.filter(trainees=obj)
        return ProgramListSerializer(programs, many=True).data

    def get_workouts(self, obj):
        workouts = Workout.objects.filter(trainees=obj)
        return WorkoutListSerializer(workouts, many=True).data

    # def get_reviews(self, obj):
    #     reviews = Review.objects.filter(trainee=obj)
    #     return ReviewsDetailSerializer(reviews, many=True).data


class TransformationAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transformations
        fields = [
            "file",
            "details",
        ]
        extra_kwargs = {
            "file": {"required": True},
            "details": {"required": True},
        }

    def create(self, validated_data):
        user = self.context["request"].user
        if not user.is_trainer:
            raise serializers.ValidationError(
                "Only trainers can create a transformation."
            )
        return Transformations.objects.create(trainer=user.trainer, **validated_data)


class TansformationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transformations
        fields = [
            "file",
            "details",
        ]
        extra_kwargs = {
            "file": {"required": False},
            "details": {"required": False},
        }

    def update(self, instance, validated_data):
        instance.before_picture = validated_data.get(
            "before_picture", instance.before_picture
        )
        instance.after_picture = validated_data.get(
            "after_picture", instance.after_picture
        )
        instance.details = validated_data.get("details", instance.details)
        instance.save()
        return instance


class TransformationsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Transformations
        fields = [
            "file",
            "details",
            "created_at",
            "updated_at",
        ]


class TrainerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    workouts = serializers.SerializerMethodField()
    programs = serializers.SerializerMethodField()
    sessions = serializers.SerializerMethodField()
    reviews = ReviewsDetailSerializer(many=True)
    transformations = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = [
            "user",
            "slug",
            "bio",
            "sport_field",
            "id_card",
            "background_image",
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
            "programs",
            "workouts",
            "sessions",
            "transformations",
            "avg_ratings",
            "number_of_ratings",
        ]

    def get_workouts(self, obj):
        workouts = Workout.objects.filter(trainer=obj)
        return WorkoutListSerializer(workouts, many=True).data

    def get_programs(self, obj):
        traienrs = TrainerProgramsHomeSerializer
        programs = Program.objects.filter(trainer=obj)
        return ProgramListSerializer(programs, many=True).data

    def get_transformations(self, obj):
        transformations = Transformations.objects.filter(trainer=obj)
        return TransformationsSerializer(transformations, many=True).data

    def get_sessions(self, obj):
        sessions = Session.objects.filter(trainer=obj)
        return SessionSerializer(sessions, many=True).data


class ProgramPlanSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

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


class TraineeProgramDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewsDetailSerializer(many=True)
    program_plans = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Program
        fields = [
            "id",
            "title",
            "picture",
            "description",
            "level",
            "type",
            "target_gender",
            "min_age",
            "max_age",
            "program_plans",
            "current_trainees_count",
            "program_capacity",
            "avg_ratings",
            "number_of_ratings",
            "reviews",
            "created_at",
            "updated_at",
        ]

    def get_program_plans(self, obj):
        if "program_plan" in self.context:
            program_plans = [self.context["program_plan"]]
        else:
            program_plans = ProgramPlan.objects.filter(program=obj)
        return ProgramPlanSerializer(program_plans, many=True).data

    def to_representation(self, instance):
        representation = super(Program, self).to_representation(instance)
        picture = representation.get("picture", None)
        if picture and not picture.startswith("http"):
            representation["picture"] = settings.BASE_URL + picture

        return representation


class TrainerProgramDetailSerializer(serializers.ModelSerializer):
    trainees = TrainerTraineeSerializer(many=True)
    reviews = ReviewsDetailSerializer(many=True)
    program_plans = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Program
        fields = [
            "id",
            "title",
            "picture",
            "description",
            "level",
            "type",
            "target_gender",
            "min_age",
            "max_age",
            "program_plans",
            "trainees",
            "current_trainees_count",
            "program_capacity",
            "avg_ratings",
            "number_of_ratings",
            "reviews",
            "created_at",
            "updated_at",
        ]

    def get_program_plans(self, obj):
        if "program_plan" in self.context:
            program_plans = [self.context["program_plan"]]
        else:
            program_plans = ProgramPlan.objects.filter(program=obj)
        return ProgramPlanSerializer(program_plans, many=True).data


class ProgramListSerializer(serializers.ModelSerializer):
    program_plans = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Program
        fields = [
            "id",
            "title",
            "picture",
            "description",
            "type",
            "current_trainees_count",
            "program_capacity",
            "program_plans",
            "avg_ratings",
            "number_of_ratings",
            "created_at",
            "updated_at",
        ]

    def get_program_plans(self, obj):
        program_plans = ProgramPlan.objects.filter(program=obj).first()
        return ProgramPlanSerializer(program_plans).data if program_plans else None

    def to_representation(self, instance):
        representation = super(ProgramListSerializer, self).to_representation(instance)
        picture = representation.get("picture", None)
        if picture and not picture.startswith("http"):
            representation["picture"] = settings.BASE_URL + picture

        return representation


class ProgramPlanAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramPlan
        fields = [
            "duration_in_weeks",
            "price",
            "is_offer",
            "offer_price",
            "max_trainees",
        ]
        extra_kwargs = {
            "duration_in_weeks": {"required": True},
            "price": {"required": True},
            "is_offer": {"required": False},
            "offer_price": {"required": False},
            "max_trainees": {"required": False},
        }


class ProgramAddSerializer(serializers.ModelSerializer):
    program_plans = ProgramPlanAddSerializer(many=True)

    class Meta:
        model = Program
        fields = [
            "title",
            "program_capacity",
            "picture",
            "level",
            "type",
            "sport_field",
            "description",
            "target_gender",
            "min_age",
            "max_age",
            "program_plans",
        ]
        extra_kwargs = {
            "program_capacity": {"required": False},
            "min_age": {"required": False},
            "max_age": {"required": False},
            "program_plans": {"required": True},
        }

    def create(self, validated_data):
        user = self.context["request"].user
        if not user.is_trainer:
            raise serializers.ValidationError("Only trainers can create a program.")
        program_plans_data = validated_data.pop("program_plans")
        program = Program.objects.create(**validated_data)
        for program_plan_data in program_plans_data:
            ProgramPlan.objects.create(program=program, **program_plan_data)
        return program


class ProgramPlanUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProgramPlan
        fields = [
            "id",
            "duration_in_weeks",
            "price",
            "is_offer",
            "offer_price",
            "max_trainees",
        ]
        extra_kwargs = {
            "id": {"required": False},
            "duration_in_weeks": {"required": False},
            "price": {"required": False},
            "is_offer": {"required": False},
            "offer_price": {"required": False},
            "max_trainees": {"required": False},
        }


class ProgramUpdateSerializer(serializers.ModelSerializer):
    program_plans = ProgramPlanUpdateSerializer(many=True)

    class Meta:
        model = Program
        fields = [
            "id",
            "title",
            "program_capacity",
            "picture",
            "level",
            "type",
            "sport_field",
            "description",
            "target_gender",
            "min_age",
            "max_age",
            "program_plans",
        ]
        extra_kwargs = {
            "title": {"required": False},
            "program_capacity": {"required": False},
            "picture": {"required": False},
            "level": {"required": False},
            "type": {"required": False},
            "sport_field": {"required": False},
            "description": {"required": False},
            "target_gender": {"required": False},
            "min_age": {"required": False},
            "max_age": {"required": False},
            "program_plans": {"required": False},
        }

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.program_capacity = validated_data.get(
            "program_capacity", instance.program_capacity
        )
        instance.picture = validated_data.get("picture", instance.picture)
        instance.level = validated_data.get("level", instance.level)
        instance.type = validated_data.get("type", instance.type)
        instance.sport_field = validated_data.get("sport_field", instance.sport_field)
        instance.description = validated_data.get("description", instance.description)
        instance.target_gender = validated_data.get(
            "target_gender", instance.target_gender
        )
        instance.min_age = validated_data.get("min_age", instance.min_age)
        instance.max_age = validated_data.get("max_age", instance.max_age)

        program_plans_data = validated_data.pop("program_plans", None)
        if program_plans_data is not None:
            program_plans = instance.program_plans.all()
            program_plans = list(program_plans)

            for program_plan_data in program_plans_data:

                program_plan_id = program_plan_data.get("id", None)
                print("program_plan_id", program_plan_id)
                if program_plan_id:
                    try:
                        program_plan = ProgramPlan.objects.get(id=program_plan_id)
                        serializer = ProgramPlanUpdateSerializer(
                            program_plan, data=program_plan_data, partial=True
                        )
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                    except ProgramPlan.DoesNotExist:
                        raise serializers.ValidationError(
                            {"program_plan": "Program plan does not exist."}
                        )
                else:
                    ProgramPlan.objects.create(program=instance, **program_plan_data)
        instance.save()
        return instance


class WokroutAddFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutFile
        fields = [
            "file_or_video",
            "title",
            "details",
        ]
        extra_kwargs = {
            "file_or_video": {"required": False},
            "title": {"required": True},
            "details": {"required": False},
        }


class WokroutUpdateFileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = WorkoutFile
        fields = [
            "id",
            "file_or_video",
            "title",
            "details",
        ]
        extra_kwargs = {
            "id": {"required": True},
            "file_or_video": {"required": False},
            "title": {"required": True},
            "details": {"required": False},
        }


class WorkoutAddSerializer(serializers.ModelSerializer):
    workout_files = WokroutAddFileSerializer(many=True)

    class Meta:
        model = Workout
        fields = [
            "title",
            "picture",
            "description",
            "level",
            "target_gender",
            "price",
            "min_age",
            "max_age",
            "is_offer",
            "offer_price",
            "sport_field",
            "workout_files",
        ]
        extra_kwargs = {
            "title": {"required": True},
            "description": {"required": True},
            "price": {"required": True},
            "sport_field": {"required": True},
            "workout_files": {"required": False},
        }

    def create(self, validated_data):
        user = self.context["request"].user
        if not user.is_trainer:
            raise serializers.ValidationError("Only trainers can create a program.")
        workout_files_data = validated_data.pop("workout_files")
        workout = Workout.objects.create(**validated_data)
        for workout_file_data in workout_files_data:
            WorkoutFile.objects.create(workout=workout, **workout_file_data)
        return workout


class WorkoutUpdateSerializer(serializers.ModelSerializer):
    workout_files = WokroutUpdateFileSerializer(many=True)

    class Meta:
        model = Workout
        fields = [
            "title",
            "picture",
            "description",
            "level",
            "target_gender",
            "price",
            "min_age",
            "max_age",
            "is_offer",
            "offer_price",
            "sport_field",
            "workout_files",
        ]
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "price": {"required": False},
            "sport_field": {"required": False},
            "workout_files": {"required": False},
        }

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.picture = validated_data.get("picture", instance.picture)
        instance.description = validated_data.get("description", instance.description)
        instance.level = validated_data.get("level", instance.level)
        instance.target_gender = validated_data.get(
            "target_gender", instance.target_gender
        )
        instance.price = validated_data.get("price", instance.price)
        instance.min_age = validated_data.get("min_age", instance.min_age)
        instance.max_age = validated_data.get("max_age", instance.max_age)
        instance.is_offer = validated_data.get("is_offer", instance.is_offer)
        instance.offer_price = validated_data.get("offer_price", instance.offer_price)
        instance.sport_field = validated_data.get("sport_field", instance.sport_field)

        workout_files_data = validated_data.pop("workout_files", None)
        if workout_files_data is not None:
            workout_files = instance.workout_files.all()
            workout_files = list(workout_files)

            for workout_file_data in workout_files_data:
                workout_file_id = workout_file_data.get("id", None)
                if workout_file_id:
                    try:
                        workout_file = WorkoutFile.objects.get(id=workout_file_id)
                        serializer = WokroutUpdateFileSerializer(
                            workout_file, data=workout_file_data, partial=True
                        )
                        if serializer.is_valid():
                            serializer.save()
                    except WorkoutFile.DoesNotExist:
                        pass
                else:
                    WorkoutFile.objects.create(workout=instance, **workout_file_data)
        return instance


class WorkoutFileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = WorkoutFile
        fields = [
            "file_or_video",
            "video_duration",
            "title",
            "details",
            "created_at",
            "updated_at",
        ]


class TraineeWorkoutDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewsDetailSerializer(many=True)
    workout_videos_files = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

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
            "is_offer",
            "offer_price",
            "sport_field",
            "workout_videos_files",
            "number_of_videos",
            "current_trainees_count",
            "duration_in_minutes",
            "avg_ratings",
            "number_of_ratings",
            "reviews",
            "created_at",
            "updated_at",
        ]

    def get_workout_videos_files(self, obj):
        workout_videos_files = WorkoutFile.objects.filter(workout=obj)
        if self.context.get("request").user in obj.trainees.all():
            return WorkoutFileSerializer(workout_videos_files, many=True).data
        else:
            return WorkoutFileSerializer(workout_videos_files.first()).data
    
    def to_representation(self, instance):
        representation = super(Workout, self).to_representation(instance)
        picture = representation.get("picture", None)
        if picture and not picture.startswith("http"):
            representation["picture"] = settings.BASE_URL + picture

        return representation

class TrainerWorkoutDetailSerializer(serializers.ModelSerializer):
    trainees = TraineeSerializer(many=True)
    reviews = ReviewsDetailSerializer(many=True)
    workout_videos_files = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

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
            "is_offer",
            "offer_price",
            "sport_field",
            "workout_videos_files",
            "number_of_videos",
            "current_trainees_count",
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


class PackageUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = [
            "session_type",
            "is_active",
            "price",
        ]
        extra_kwargs = {
            "session_type": {"required": True},
            "is_active": {"required": False},
            "price": {"required": False},
        }


class SessionSettingsUpdateSerializer(serializers.ModelSerializer):
    package = PackageUpdateSerializer(many=True)

    class Meta:
        model = Session
        fields = [
            "package",
            "duration",
            "target_gender",
            "min_age",
            "max_age",
            "update_body_measure",
            "update_pref_lifestyle",
            "attach_body_img",
            "attach_med_report",
        ]
        extra_kwargs = {
            "package": {"required": False},
            "duration": {"required": True},
            "target_gender": {"required": False},
            "min_age": {"required": False},
            "max_age": {"required": False},
            "update_body_measure": {"required": False},
            "update_pref_lifestyle": {"required": False},
            "attach_body_img": {"required": False},
            "attach_med_report": {"required": False},
        }

    def update(self, instance, validated_data):
        instance.duration = validated_data.get("duration", instance.duration)
        instance.target_gender = validated_data.get(
            "target_gender", instance.target_gender
        )
        instance.min_age = validated_data.get("min_age", instance.min_age)
        instance.max_age = validated_data.get("max_age", instance.max_age)
        instance.update_body_measure = validated_data.get(
            "update_body_measure", instance.update_body_measure
        )
        instance.update_pref_lifestyle = validated_data.get(
            "update_pref_lifestyle", instance.update_pref_lifestyle
        )
        instance.attach_body_img = validated_data.get(
            "attach_body_img", instance.attach_body_img
        )
        instance.attach_med_report = validated_data.get(
            "attach_med_report", instance.attach_med_report
        )

        package_data = validated_data.pop("package", None)
        if package_data is not None:
            for package_item in package_data:
                session_type = package_item.get("session_type", None)
                if session_type:
                    package = Package.objects.get(
                        session_type=session_type, session=instance
                    )
                    package.session_type = package_item.get(
                        "session_type", package.session_type
                    )
                    package.is_active = package_item.get("is_active", package.is_active)
                    package.price = package_item.get("price", package.price)
                    package.save()
                else:
                    raise serializers.ValidationError("Session type is required.")
            instance.save()
            return instance


class TimeAddSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Time
        fields = [
            "id",
            "from_time",
            "to_time",
        ]
        extra_kwargs = {
            "id": {"required": False},
            "from_time": {"required": True},
            "to_time": {"required": True},
        }


class AvailabilityUpdateSerializer(serializers.ModelSerializer):
    time = TimeAddSerializer(many=True, required=False)

    class Meta:
        model = Availability
        fields = [
            "time",
            "is_active",
        ]
        extra_kwargs = {
            "is_active": {"required": False},
        }

    def update(self, instance, validated_data):
        instance.is_active = validated_data.get("is_active", instance.is_active)
        print("instance", instance)
        time_data = validated_data.pop("time", None)
        if time_data is not None:
            for time_item in time_data:
                time_id = time_item.get("id", None)
                from_time = time_item.get("from_time", None)
                to_time = time_item.get("to_time", None)

                if from_time and to_time:
                    if Time.objects.filter(
                        from_time=from_time, to_time=to_time
                    ).exists():
                        raise serializers.ValidationError("Time slot already exists.")

                if time_id:
                    time = Time.objects.get(id=time_id)
                    time.from_time = from_time if from_time else time.from_time
                    time.to_time = to_time if to_time else time.to_time
                    time.save()
                else:
                    Time.objects.create(availability=instance, **time_item)
        instance.save()
        return instance


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
            "id",
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
        time = Time.objects.filter(availability=obj)
        return TimeSerializer(time, many=True).data


class SessionSerializer(serializers.ModelSerializer):
    package = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

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
            "created_at",
            "updated_at",
        ]

    def get_package(self, obj):
        package = Package.objects.filter(session=obj)
        return PackageSerializer(package, many=True).data

    def get_availability(self, obj):
        try:
            availability = Availability.objects.filter(session=obj)
            serializer = AvialabilitySerializer(availability, many=True).data
            return serializer
        except Exception as e:
            raise serializers.ValidationError(str(e))


class PaymentAddSerializer(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(
        choices=["program", "workout", "session", "club"],
        required=True,
        error_messages={
            "invalid_choice": "Invalid content type. Must be program, workout, session or club."
        },
    )

    object_id = serializers.IntegerField(required=True)

    class Meta:
        model = Payment
        fields = [
            "amount",
            "method",
            "status",
            "transaction_id",
            "content_type",
            "object_id",
        ]

    def validate(self, data):
        user = self.context["request"].user
        trainee = Trainee.objects.get(user=user)
        content_type = data.get("content_type")
        object_id = data.get("object_id")
        if data.get("method") != "cash" and not data.get("status") != "pending":
            raise serializers.ValidationError(
                "Only payments with the 'cash' method can be pending."
            )
        if content_type == "program":
            content_type = ContentType.objects.get_for_model(Program)
        elif content_type == "workout":
            content_type = ContentType.objects.get_for_model(Workout)
        elif content_type == "session":
            content_type = ContentType.objects.get_for_model(Session)
        elif content_type == "club":
            content_type = ContentType.objects.get_for_model(Club)
        elif content_type == "program_plan":
            content_type = ContentType.objects.get_for_model(ProgramPlan)

        # Check if the payment already exists
        if Payment.objects.filter(
            content_type=content_type, object_id=object_id, trainee=trainee
        ).exists():
            raise serializers.ValidationError("This payment already exists.")

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        trainee = Trainee.objects.get(user=user)
        content_type = validated_data.pop("content_type")
        object_id = validated_data.pop("object_id")
        if not user.is_trainee:
            raise serializers.ValidationError("Only trainees can make a payment.")
        if content_type == "program":
            content_type = ContentType.objects.get_for_model(Program)
        elif content_type == "workout":
            content_type = ContentType.objects.get_for_model(Workout)
        elif content_type == "session":
            content_type = ContentType.objects.get_for_model(Session)
        elif content_type == "club":
            content_type = ContentType.objects.get_for_model(Club)

        return Payment.objects.create(
            content_type=content_type, object_id=object_id, **validated_data
        )


class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "amount",
            "method",
            "status",
            "transaction_id",
        ]
        extra_kwargs = {
            "amount": {"required": False},
            "method": {"required": True},
            "status": {"required": False},
            "transaction_id": {"required": False},
        }

    def validate(self, data):
        if data.get("method") != "cash":
            raise serializers.ValidationError(
                "Only payments with the 'cash' method can be updated."
            )
        return data

    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount", instance.amount)
        instance.method = validated_data.get("method", instance.method)
        instance.status = validated_data.get("status", instance.status)
        instance.transaction_id = validated_data.get(
            "transaction_id", instance.transaction_id
        )
        instance.save()
        return instance


class PaymentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "trainee",
            "amount",
            "method",
            "status",
            "transaction_id",
            "content_type",
            "object_id",
            "created_at",
            "updated_at",
        ]


class JoinProgramPlanSerializer(serializers.Serializer):
    program_plan_id = serializers.IntegerField(
        required=True,
        error_messages={"required": "Program plan id is required."},
    )

    def validate(self, data):
        user = self.context["request"].user
        program_plan_id = data.get("program_plan_id")
        program_plan = ProgramPlan.objects.get(id=program_plan_id)
        program = Program.objects.get(id=program_plan.program.id)
        if program.trainees.filter(user=user).exists():
            raise serializers.ValidationError("You are already in this program.")
        if (
            program.program_capacity is not None
            and program.program_capacity <= program.current_trainees_count
        ):
            raise serializers.ValidationError("This program is full.")
        if (
            program_plan.max_trainees is not None
            and program_plan.max_trainees <= program_plan.current_trainees_count
        ):
            raise serializers.ValidationError("This program plan is full.")
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        trainee = Trainee.objects.get(user=user)
        program_plan_id = validated_data.get("program_plan_id")
        program_plan = ProgramPlan.objects.get(id=program_plan_id)
        program = Program.objects.get(id=program_plan.program.id)
        trainer = Trainer.objects.get(user=program.trainer.user)
        amount = program_plan.price
        trainer.current_balance += amount
        trainer.total_balance += amount
        program.current_trainees_count += 1
        print("program.current_trainees_count", program.current_trainees_count)
        program_plan.current_trainees_count += 1
        program_plan.save()
        program.trainees.add(trainee)
        program.save()
        trainer.save()
        return program_plan.program


class JoinWorkoutSerializer(serializers.Serializer):
    workout_id = serializers.IntegerField(
        required=True,
        error_messages={"required": "Workout id is required."},
    )

    def validate(self, data):
        user = self.context["request"].user
        workout_id = data.get("workout_id")
        workout = Workout.objects.get(id=workout_id)
        if workout.trainees.filter(user=user).exists():
            raise serializers.ValidationError("You are already in this workout.")
        if (
            workout.workout_capacity is not None
            and workout.workout_capacity <= workout.current_trainees_count
        ):
            raise serializers.ValidationError("This workout is full.")
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        trainee = Trainee.objects.get(user=user)
        workout_id = validated_data.get("workout_id")
        workout = Workout.objects.get(id=workout_id)
        trainer = Trainer.objects.get(user=workout.trainer.user)
        amount = workout.price
        trainer.current_balance += amount
        trainer.total_balance += amount
        workout.current_trainees_count += 1
        workout.save()
        workout.trainees.add(trainee)
        trainer.save()
        return workout


class ClientRequestAddSerializer(serializers.ModelSerializer):
    program_plan = serializers.IntegerField(
        required=True,
        error_messages={"required": "Program plan id is required."},
    )

    class Meta:
        model = ClientRequest
        fields = [
            "program_plan",
        ]
        extra_kwargs = {
            "program_plan": {"required": True},
        }

    def validate(self, data):
        user = self.context["request"].user
        trainee = Trainee.objects.get(user=user)
        program_plan = ProgramPlan.objects.get(id=data.get("program_plan"))
        print("reached here")
        if ClientRequest.objects.filter(
            trainee=trainee, program_plan=program_plan, status="pending"
        ).exists():
            raise serializers.ValidationError(
                "You have already requested this program."
            )
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        trainee = Trainee.objects.get(user=user)
        program_plan = ProgramPlan.objects.get(id=validated_data.get("program_plan"))
        return ClientRequest.objects.create(trainee=trainee, program_plan=program_plan)


class ClientRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientRequest
        fields = [
            "message",
            "status",
        ]

    def validate(self, data):
        user = self.context["request"].user

        if not data.get("status") in ["accepted", "rejected"]:
            raise serializers.ValidationError("Invalid status.")
        return data

    def update(self, instance, validated_data):
        print("reached here")
        instance.message = validated_data.get("message", instance.message)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class TraineeUpdateSerializer(serializers.ModelSerializer):
    user = CustomUserUpdateSerializer()

    class Meta:
        model = Trainee
        fields = [
            "user",
            "height",
            "weight",
            "fitness_goals",
            "current_physical_level",
        ]
        extra_kwargs = {
            "user": {"required": False},
            "height": {"required": False},
            "weight": {"required": False},
            "fitness_goals": {"required": False},
            "current_physical_level": {"required": False},
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        with transaction.atomic():
            if user_data is not None:
                user_serailizer = CustomUserUpdateSerializer(
                    instance.user, data=user_data
                )
                if user_serailizer.is_valid(raise_exception=True):
                    user_serailizer.update(instance.owner, user_data)
            instance.height = validated_data.get("height", instance.height)
            instance.weight = validated_data.get("weight", instance.weight)
            instance.fitness_goals = validated_data.get(
                "fitness_goals", instance.fitness_goals
            )
            instance.current_physical_level = validated_data.get(
                "current_physical_level", instance.current_physical_level
            )
            instance.save()


class TrainerUpdateSerializer(serializers.ModelSerializer):
    user = CustomUserUpdateSerializer()

    class Meta:
        model = Trainer
        fields = [
            "user",
            "bio",
            "sport_field",
            "id_card",
            "exp_injuries",
            "physical_disabilities",
            "experience",
            "languages",
            "facebook_url",
            "instagram_url",
            "youtube_url",
        ]
        extra_kwargs = {
            "user": {"required": False},
            "bio": {"required": False},
            "sport_field": {"required": False},
            "id_card": {"required": False},
            "exp_injuries": {"required": False},
            "physical_disabilities": {"required": False},
            "experience": {"required": False},
            "languages": {"required": False},
            "facebook_url": {"required": False},
            "instagram_url": {"required": False},
            "youtube_url": {"required": False},
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        with transaction.atomic():
            if user_data is not None:
                user_serailizer = CustomUserUpdateSerializer(
                    instance.user, data=user_data
                )
                if user_serailizer.is_valid(raise_exception=True):
                    user_serailizer.update(instance.owner, user_data)
            instance.bio = validated_data.get("bio", instance.bio)
            instance.sport_field = validated_data.get(
                "sport_field", instance.sport_field
            )
            instance.id_card = validated_data.get("id_card", instance.id_card)
            instance.exp_injuries = validated_data.get(
                "exp_injuries", instance.exp_injuries
            )
            instance.physical_disabilities = validated_data.get(
                "physical_disabilities", instance.physical_disabilities
            )
            instance.experience = validated_data.get("experience", instance.experience)
            instance.languages = validated_data.get("languages", instance.languages)
            instance.facebook_url = validated_data.get(
                "facebook_url", instance.facebook_url
            )
            instance.instagram_url = validated_data.get(
                "instagram_url", instance.instagram_url
            )
            instance.youtube_url = validated_data.get(
                "youtube_url", instance.youtube_url
            )
            instance.save()


class ClientRequestTraineeSerializer(serializers.ModelSerializer):
    program = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ClientRequest
        fields = [
            "id",
            "program",
            "message",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_program(self, obj):
        program = Program.objects.get(id=obj.program_plan.program.id)
        return TraineeProgramDetailSerializer(
            program, context={"program_plan": obj.program_plan}
        ).data


class ClientRequestTrainerSerializer(serializers.ModelSerializer):
    trainee = TraineeSerializer()
    program = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ClientRequest
        fields = [
            "id",
            "trainee",
            "program",
            "message",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_program(self, obj):
        program = Program.objects.get(id=obj.program_plan.program.id)
        return TrainerProgramDetailSerializer(
            program, context={"program_plan": obj.program_plan}
        ).data


class ReviewAddSerializer(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(
        choices=["program", "workout", "trainer", "club"],
        required=True,
        error_messages={
            "invalid_choice": "Invalid content type. Must be program, workout, session or club."
        },
    )
    object_id = serializers.IntegerField(required=True)

    class Meta:
        model = Review
        fields = [
            "ratings",
            "comment",
            "content_type",
            "object_id",
        ]
        extra_kwargs = {
            "ratings": {"required": True},
            "comment": {"required": False},
            "cotent_type": {"required": True},
            "object_id": {"required": True},
        }

    def validate(self, data):
        user = self.context["request"].user
        trainee = Trainee.objects.get(user=user)
        content_type = data.get("content_type")
        object_id = data.get("object_id")
        if content_type == "program":
            content_type = ContentType.objects.get_for_model(Program)
        elif content_type == "workout":
            content_type = ContentType.objects.get_for_model(Workout)
        elif content_type == "trainer":
            content_type = ContentType.objects.get_for_model(Trainer)
        elif content_type == "club":
            content_type = ContentType.objects.get_for_model(Club)

        # Check if the review already exists
        if Review.objects.filter(
            content_type=content_type, object_id=object_id, trainee=trainee
        ).exists():
            raise serializers.ValidationError("This review already exists.")

    def create(self, validated_data):
        user = self.context["request"].user
        trainee = Trainee.objects.get(user=user)
        content_type = validated_data.pop("content_type")
        object_id = validated_data.pop("object_id")
        if not user.is_trainee:
            raise serializers.ValidationError("Only trainees can make a review.")
        if content_type == "program":
            content_type = ContentType.objects.get_for_model(Program)
        elif content_type == "workout":
            content_type = ContentType.objects.get_for_model(Workout)
        elif content_type == "trainer":
            content_type = ContentType.objects.get_for_model(Trainer)
        elif content_type == "club":
            content_type = ContentType.objects.get_for_model(Club)

        return Review.objects.create(
            content_type=content_type,
            object_id=object_id,
            trainee=trainee,
            **validated_data
        )


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "ratings",
            "comment",
        ]
        extra_kwargs = {
            "ratings": {"required": False},
            "comment": {"required": False},
        }

    def validate(self, data):
        user = self.context["request"].user
        trainee = Trainee.objects.get(user=user)
        if not Review.objects.filter(id=self.instance.id, trainee=trainee).exists():
            raise serializers.ValidationError("You can only update your own reviews.")
        if data.get("ratings") < 1 or data.get("ratings") > 5:
            raise serializers.ValidationError("Ratings must be between 1 and 5.")
        return data

    def update(self, instance, validated_data):
        instance.ratings = validated_data.get("ratings", instance.ratings)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance
