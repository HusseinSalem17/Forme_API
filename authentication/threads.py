from django.core.mail import EmailMessage

from rest_framework import status

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
            html_content=message,
        )

        try:
            # Send the email
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(msg)
        except Exception as e:
            print(e)
            return Response(
                {"error": "Unable to send otp"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "message": "We have sent otp to your email!",
            },
            status=status.HTTP_200_OK,
        )

    # def send_contact_email(sender_email, message_body):
    #     """
    #     Send a contact us message from a verified sender email, with the user's email as reply-to.
    #     """
    #     subject = "Contact Us Message"
    #     receiver_email = "husseinsalem910@gmail.com"
    #     verified_sender_email = "husseinsalem177@gmail.com"  # This should be a verified sender email in your SendGrid account

    #     # Create context for email template
    #     context = {
    #         "sender_email": sender_email,
    #         "message_body": message_body,
    #         "date": datetime.datetime.now().strftime("%d %B, %Y"),
    #     }

    #     # Assuming get_template is a function you've defined elsewhere to get your email templates
    #     message = get_template("emails/contact-us-template.html").render(context)

    #     # Create SendGrid Mail object with a verified sender and user's email as reply-to
    #     msg = Mail(
    #         from_email=verified_sender_email,
    #         to_emails=receiver_email,
    #         subject=subject,
    #         html_content=message
    #     )
    #     msg.reply_to = sender_email  # Set the user's email as reply-to

    #     try:
    #         # Send the email
    #         sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    #         response = sg.send(msg)
    #         print('Email sent successfully')
    #     except Exception as e:
    #         print("Error: ", e.__str__())
    #         return (
    #             {"error": "Unable to send message"},
    #             500,  # Assuming you're using a framework that expects a status code here
    #         )

    #     return (
    #         {"message": "Your message has been sent successfully!"},
    #         201,  # Assuming you're using a framework that expects a status code here
    #     )
        
