import datetime
from rest_framework.decorators import api_view, permission_classes

from account.models import CustomUser, Trainee
from trainings.models import Trainer
from .models import OTP, Token
from .utils import send_otp, token_response, IsAuthenticatedUser
from django.shortcuts import get_object_or_404

from rest_framework.response import Response


# Create your views here.
@api_view(["POST"])
def request_otp(request):
    email = request.data.get("email")

    if email:
        if CustomUser.objects.filter(email=email).exists():
            return Response({"detail": "email already exists"}, status=400)
        return send_otp(email)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
def resend_otp(request):
    email = request.data.get("email")
    if email:
        return send_otp(email)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
def verify_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    if email and otp:
        otp_obj = get_object_or_404(OTP, email=email, verified=False)
        if otp_obj.validity.replace(tzinfo=None) > datetime.datetime.utcnow():
            print(otp_obj.validity, otp_obj.otp)
            if otp_obj.otp == int(otp):
                otp_obj.verified = True
                otp_obj.save()
                return Response("otp verified successfully", status=200)
            else:
                print(otp_obj.otp, otp)
                return Response({"detail": "Incorrect otp"}, status=400)
        else:
            return Response({"detail": "otp expired"}, status=400)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
def reset_password(request):
    email = request.data.get("email")
    new_password = request.data.get("new_password")

    if email and new_password:
        user = get_object_or_404(CustomUser, email=email)
        user.set_password(new_password)
        user.save()
        return Response("Password reset successfully", status=200)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def change_password(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if old_password and new_password:
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response("Password changed successfully", status=200)
        else:
            return Response({"detail": "Incorrect old password"}, status=400)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
def create_account(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user_type = request.data.get("user_type")

    if user_type and email and password:
        try:
            if user_type == "trainer":
                user = CustomUser.objects.create_trainer(
                    email,
                    password,
                )
                Trainer.objects.create(
                    user=user,
                )
            elif user_type == "trainee":
                user = CustomUser.objects.create_trainee(
                    email,
                    password,
                )
                Trainee.objects.create(
                    user=user,
                )
            return token_response(user)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email and password:
        user = get_object_or_404(CustomUser, email=email)
        if user and user.check_password(password):
            return token_response(user)
        else:
            return Response({"detail": "Invalid credentials"}, status=400)
    else:
        return Response({"detail": "Invalid data provided"}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticatedUser])
def logout(request):
    user = request.user
    token = get_object_or_404(Token, user=user)
    token.delete()
    return Response("Logged out successfully", status=200)
