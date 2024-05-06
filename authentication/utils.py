from django.core.mail import EmailMessage


import threading

from django.template.loader import get_template
from django.core.mail import EmailMessage
from rest_framework.response import Response

from random import randint
import datetime

from forme import settings
from .models import OTP

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        EmailThread(email).start()

    def change_otp_verify(email):
        """
        Change the OTP state to verified
        """
        otp = OTP.objects.filter(email=email)
        if otp.exists():
            otp = otp.first()
            otp.verified = True
            otp.save()
            return True
        return False

    def delete_otp(email):
        """
        Delete the OTP
        """
        otp = OTP.objects.filter(email=email)
        if otp.exists():
            otp.delete()
            return True
        return False

    def check_otp_verified(email):
        """
        Check if the OTP is verified
        """
        otp = OTP.objects.filter(email=email)
        if otp.exists():
            otp = otp.first()
            return otp.verified
        return False

    def check_otp_validality(email):
        """
        Check if the OTP is valid
        """
        otp = OTP.objects.filter(email=email)
        if otp.exists():
            otp = otp.first()
            if otp.validity.replace(tzinfo=None) > datetime.datetime.utcnow():
                return True
            return False
        return True

    # def send_otp(email):
    #     """
    #     Send OTP to the user's email
    #     """
    #     print("reached here1")
    #     otp = randint(1000, 9999)
    #     subject = "Your OTP for Forme"
    #     validity = datetime.datetime.now() + datetime.timedelta(minutes=10)

    #     # Generate the URL for the logo in the media folder
    #     logo_url = settings.MEDIA_URL + "Logo-scaled.svg"
    #     # Create context for email template
    #     context = {
    #         "otp": otp,
    #         "validity": validity,
    #         "verified": False,
    #         "logo_url": logo_url,  # Replace with the actual URL of your logo
    #         "date": datetime.datetime.now().strftime("%d %B, %Y"),
    #     }

    #     # Render email template
    #     message = get_template("emails/email-template.html").render(context)
    #     print("reached here1.5")
    #     # Check if there's otp for this email then delete it
    #     existing_otp = OTP.objects.filter(email=email)
    #     if existing_otp.exists():
    #         existing_otp.delete()

    #     # Create a new OTP
    #     OTP.objects.create(
    #         email=email,
    #         validity=validity,
    #         otp=otp,
    #         verified=False,
    #     )
    #     to_email = email
    #     msg = EmailMessage(
    #         subject,
    #         body=message,
    #         to=[to_email],
    #     )
    #     msg.content_subtype = "html"
    #     try:
    #         msg.send()
    #     except Exception as e:
    #         print(e)
    #         return Response({"message": "unable to send otp"}, status=400)
    #     return Response(
    #         {
    #             "message": "We have sent otp to your email!",
    #         },
    #         status=200,
    #     )


    def send_otp(email):
        """
        Send OTP to the user's email
        """
        print("reached here1")
        otp = randint(1000, 9999)
        subject = "Your OTP for Forme"
        validity = datetime.datetime.now() + datetime.timedelta(minutes=10)

        # Generate the URL for the logo in the media folder
        logo_url = settings.MEDIA_URL + "Logo-scaled.svg"
        # Create context for email template
        context = {
            "otp": otp,
            "validity": validity,
            "verified": False,
            "logo_url": logo_url,  # Replace with the actual URL of your logo
            "date": datetime.datetime.now().strftime("%d %B, %Y"),
        }

        # Render email template
        message = get_template("emails/email-template.html").render(context)
        print("reached here1.5")
        # Check if there's otp for this email then delete it
        existing_otp = OTP.objects.filter(email=email)
        if existing_otp.exists():
            existing_otp.delete()

        # Create a new OTP
        OTP.objects.create(
            email=email,
            validity=validity,
            otp=otp,
            verified=False,
        )
        to_email = email

        # Create SendGrid Mail object
        msg = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=message
        )

        try:
            # Send the email
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(msg)
        except Exception as e:
            print(e)
            return Response({"message": "unable to send otp"}, status=400)

        return Response(
            {
                "message": "We have sent otp to your email!",
            },
            status=200,
        )





# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)

#     # Now add the HTTP status code to the response.
#     if response is not None:
#         response.data["status_code"] = response.status_code

#     return response
