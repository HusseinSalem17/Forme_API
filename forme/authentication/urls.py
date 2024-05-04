# urls.py
from django.urls import path
from .views import (
    CompleteProfileTraineeView,
    CompleteProfileTrainerView,
    DeleteAccountView,
    ForgetPasswordView,
    LocationView,
    LoginView,
    LogoutAPIView,
    ResetPasswordView,
    RegisterView,
    RegisterView,
    RequestOTPView,
    ResetPasswordView,
    SetNewPasswordView,
    UpdatePreferenceTrainerView,
    UpdatePreferenceTraineeView,
    UpdateProfilePictureView,
    VerifyOTPView,
)

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register_normal",
    ),
    path(
        "request_otp/",
        RequestOTPView.as_view(),
        name="request_otp_view",
    ),
    path(
        "verify_otp/",
        VerifyOTPView.as_view(),
        name="verify_otp_view",
    ),
    path(
        "reset_password/",
        ResetPasswordView.as_view(),
        name="reset_password_view",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "delete_account/",
        DeleteAccountView.as_view(),
        name="delete_user",
    ),
    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),
    path(
        "location/",
        LocationView.as_view(),
        name="location",
    ),
    path(
        "update_profile_picture/",
        UpdateProfilePictureView.as_view(),
        name="update_profile_picture",
    ),
    path(
        "complete_profile_trainee/",
        CompleteProfileTraineeView.as_view(),
        name="complete_profile_trainee",
    ),
    path(
        "complete_profile_trainer/",
        CompleteProfileTrainerView.as_view(),
        name="complete_profile_trainer",
    ),
    # path(
    #     "complete_profile/",
    #     CompleteProfileView.as_view(),
    #     name="complete_profile",
    # ),
    path(
        "update_preference_trainee/",
        UpdatePreferenceTraineeView.as_view(),
        name="update_preference_trainee",
    ),
    path(
        "update_preference_trainer/",
        UpdatePreferenceTrainerView.as_view(),
        name="update_preference_trainer",
    ),
    # path(
    #     "update_preference/",
    #     UpdatePreferenceView.as_view(),
    #     name="update_preference",
    # ),
    path(
        "forget_password/",
        ForgetPasswordView.as_view(),
        name="forget_password",
    ),
    path(
        "set_new_password/",
        SetNewPasswordView.as_view(),
        name="set_new_password",
    ),
]
