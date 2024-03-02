# urls.py
from django.urls import path
from .views import (
    TraineeProfileDetail,
    TraineeProfileList,
    complete_profile,
    update_preference,
)

urlpatterns = [
    path(
        "complete_profile/",
        complete_profile,
        name="complete_profile",
    ),
    path(
        "update_preference/",
        update_preference,
        name="update_preference",
    ),
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
]
