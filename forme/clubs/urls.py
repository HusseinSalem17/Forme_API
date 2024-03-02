from django.urls import path
from .views import branch_list, club_list


urlpatterns = [
    path(
        "clubs/",
        club_list,
        name="club-list",
    ),
    path(
        "branches/",
        branch_list,
        name="branch-list",
    ),
]
