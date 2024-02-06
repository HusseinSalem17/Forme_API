# from random import randint
# import datetime

# from forme.forme import settings
# from rest_framework.response import Response
# import uuid

# from forme.settings import TEMPLATES_BASE_URL
# from django.core.mail import EmailMessage
# from django.template.loader import get_template

# from django.core.mail import send_mail
# from account.models import Otp, PasswordResetToken, Token
# from rest_framework.permissions import BasePermission


# def send_otp(email):
#     """
#     Send OTP to the user's email
#     """
#     otp = randint(100000, 999999)
#     subject = "Your OTP for Forme"
#     message = f"Your OTP for Forme is {otp}"
#     validity = datetime.datetime.now() + datetime.timedelta(minutes=10)
#     Otp.objects.update_or_create(
#         email=email,
#         defaults={
#             "otp": otp,
#             "validity": validity,
#             "verified": False,
#         },
#     )
#     from_email = settings.EMAIL_HOST_USER
#     to_email = email
#     send_mail(subject, message, from_email, [to_email])
#     print("otp is {otp}")
#     return Response("OTP sent successfully!")


# def new_token():
#     """
#     Generate a new token for the user
#     """
#     return uuid.uuid4().hex


# def token_response(user):
#     """
#     Return a token response
#     """
#     token = new_token()
#     Token.objects.create(user=user, token=token)
#     return Response({"token": token})


# def send_password_reset_email(user):
#     token = new_token()
#     exp_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
#     PasswordResetToken.objects.update_or_create(
#         user=user,
#         defaults={
#             "user": user,
#             "token": token,
#             "created_at": exp_time,
#         },
#     )
#     email_data = {
#         "token": token,
#         "email": user.email,
#         "base_url": TEMPLATES_BASE_URL,
#     }

#     message = get_template("emails/reset-password.html").render(email_data)

#     msg = EmailMessage(
#         "Reset Password",
#         body=message,
#         to=[user.email],
#     )

#     msg.content_subtype = "html"

#     try:
#         msg.send()
#     except Exception as e:
#         print(e)
#         return Response("unable to send password reset email", status=400)
#     return Response("reset_password_email_sent")


# class IsAuthenticatedUser(BasePermission):
#     message = "unauthenticated_user"

#     def has_permission(self, request, view):
#         return bool(request.user)
