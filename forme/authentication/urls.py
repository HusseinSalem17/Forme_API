from django.urls import path
from .views import create_account, logout

from .views import (
    change_password,
    login,
    request_otp,
    resend_otp,
    reset_password,
    verify_otp,
)

urlpatterns = [
    path(
        "request_otp/",
        request_otp,
        name="request_otp",
    ),
    path(
        "resend_otp/",
        resend_otp,
        name="resend_otp",
    ),
    path(
        "verify_otp/",
        verify_otp,
        name="verify_otp",
    ),
    path(
        "reset_password/",
        reset_password,
        name="reset_password",
    ),
    path(
        "change_password/",
        change_password,
        name="change_password",
    ),
    path(
        "login/",
        login,
        name="login",
    ),
    path(
        "create_account/",
        create_account,
        name="create_account",
    ),
    path(
        "logout/",
        logout,
        name="logout",
    ),
]
