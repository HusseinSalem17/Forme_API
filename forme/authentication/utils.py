from rest_framework.permissions import BasePermission
from rest_framework import status
from django.template.loader import get_template
from django.core.mail import EmailMessage
from rest_framework.response import Response

from random import randint
import datetime
import uuid

from forme import settings
from .models import OTP, Token


def send_otp(email):
    """
    Send OTP to the user's email
    """
    otp = randint(1000, 9999)
    subject = "Your OTP for Forme"
    validity = datetime.datetime.now() + datetime.timedelta(minutes=10)

    # Generate the URL for the logo in the media folder
    logo_url = settings.MEDIA_URL + "logo.png"
    # Create context for email template
    context = {
        "otp": otp,
        "validity": validity,
        "verified": False,
        "logo_url": logo_url,  # Replace with the actual URL of your logo
    }

    # Render email template
    message = get_template("emails/email-template.html").render(context)

    OTP.objects.update_or_create(
        email=email,
        defaults={
            "otp": otp,
            "validity": validity,
            "verified": False,
        },
    )
    to_email = email
    msg = EmailMessage(
        subject,
        body=message,
        to=[to_email],
    )
    msg.content_subtype = "html"
    try:
        msg.send()
    except Exception as e:
        print(e)
        return Response("unable to send otp", status=400)
    print("otp is ", otp)
    return Response("OTP sent successfully!", status=200)


def new_token():
    """
    Generate a new token for the user
    """
    return uuid.uuid4().hex


def token_response(user):
    """
    Return a token response
    """
    try:
        token = new_token()
        existing_token = Token.objects.filter(user=user).first()

        if existing_token:
            # If the user has a token, update its value
            existing_token.token = token
            existing_token.save()
        else:
            # If the user doesn't have a token, create a new one
            Token.objects.create(user=user, token=token)

        return Response({"token": token}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class IsAuthenticatedUser(BasePermission):
    message = "unauthenticated_user"

    def has_permission(self, request, view):
        return bool(request.user)
