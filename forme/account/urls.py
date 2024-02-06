# urls.py

from django.urls import path
from .views import TraineeProfileListCreateView, TraineeProfileList

urlpatterns = [
    path(
        "trainee-profiles/",
        TraineeProfileListCreateView.as_view(),
        name="trainee-profile-list-create",
    ),
    path(
        "trainee-profiles/",
        TraineeProfileList,
        name="trainee-profile-list",
    ),
]
