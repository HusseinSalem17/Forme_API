from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from authentication.models import CustomUser
from .serializers import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# class GoogleSocialAuthView(GenericAPIView):

#     serializer_class = GoogleSocialAuthSerializer

#     def post(self, request):
#         """

#         POST with "auth_token"

#         Send an idtoken as from google to get user information

#         """

#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = ((serializer.validated_data)['auth_token'])
#         return Response(data, status=status.HTTP_200_OK)


# class FacebookSocialAuthView(GenericAPIView):

#     serializer_class = FacebookSocialAuthSerializer

#     def post(self, request):
#         """

#         POST with "auth_token"

#         Send an access token as from facebook to get user information

#         """

#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = ((serializer.validated_data)['auth_token'])
#         return Response(data, status=status.HTTP_200_OK)


# class TwitterSocialAuthView(GenericAPIView):
#     serializer_class = TwitterAuthSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleAuthSerializer

    @swagger_auto_schema(
        request_body=GoogleAuthSerializer,
        operation_description="Send an idtoken as from google to get user information",
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type="object", properties={"token": openapi.Schema(type="string")}
                ),
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type="object", properties={"error": openapi.Schema(type="string")}
                ),
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]

        try:
            backend = load_backend(
                load_strategy(request), "google-oauth2", redirect_uri=None
            )
        except MissingBackend:
            return Response(
                {"error": "Invalid provider"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = backend.do_auth(data)
        except BaseException as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:
            return Response({"token": user.tokens()}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST
            )


class FacebookSocialAuthView(GenericAPIView):
    serializer_class = FacebookAuthSerializer

    @swagger_auto_schema(
        request_body=FacebookAuthSerializer,
        operation_description="Send an access token as from facebook to get user information",
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type="object", properties={"token": openapi.Schema(type="string")}
                ),
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type="object", properties={"error": openapi.Schema(type="string")}
                ),
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]

        try:
            backend = load_backend(
                load_strategy(request), "facebook", redirect_uri=None
            )
        except MissingBackend:
            return Response(
                {"error": "Invalid provider"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = backend.do_auth(data)
        except BaseException as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:
            return Response({"token": user.tokens()}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST
            )
