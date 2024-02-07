# urls.py

from django.urls import path
from .views import TraineeProfileDetail, TraineeProfileList, TrainerProfileDetail, TrainerProfileList

urlpatterns = [
    path(
        "trainee_profiles/",
        TraineeProfileList,
        name="trainee_profile_list",
    ),
    path(
        "trainee_profiles/<int:pk>/",
        TraineeProfileDetail,
        name="trainee_profile_detail",
    ),
    path(
        "trainer_profiles/",
        TrainerProfileList,
        name="trainer_profile_list",
    ),
    path(
        "trainer_profiles/<int:pk>/",
        TrainerProfileDetail,
        name="trainer_profile_detail",
    ),
]
