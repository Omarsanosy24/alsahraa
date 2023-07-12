from logging import exception
from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.authentication import TokenAuthentication
from django.template.loader import render_to_string
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.http import HttpResponsePermanentRedirect
import os
from rest_framework.authtoken.models import Token
import json
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from uuid import getnode as get_mac
import uuid
from rest_framework_api_key.permissions import HasAPIKey

# Create your views here.
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [HasAPIKey]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                {
                    "status": False,
                    "message": "this email is already exist",
                    "data": None,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
                {
                    "status": True,
                    "message": "تم انشاء الحساب بنجاح",
                    "data": serializer.data,  
                },
                status=status.HTTP_200_OK,
            )


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        # except jwt.exceptions.DecodeError as identifier:
        #   return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [HasAPIKey]

    def post(self, request):

        serializer = self.serializer_class(data=request.data, context={"request": request},)
        serializer.is_valid(raise_exception=True)
        if "token" in serializer.data.keys():
            return Response(
                {
                    "status": True,
                    "message": "logged successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            r = serializer.data.get("email")
            return Response(
                {"status": False, "message": r, "data": {}}, status=status.HTTP_200_OK
            )


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get("email", "")

        if User.objects.filter(email=email).exists():
            
            return Response(
                {
                    "status": True,
                    "message": "We have sent you a link to reset your password",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": False, "message": "this email is not register"},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token is not valid, please request a new one"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return Response(
                {
                    "success": True,
                    "message": "credentials Valid",
                    "uidb64": uidb64,
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator():
                return Response(
                    {"error": "Token is not valid, please request a new one"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {"status": True, "message": "logout done"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": False, "message": "invalid  token"},
                status=status.HTTP_200_OK,
            )

class TokenView(generics.GenericAPIView):
    serializer_class = TokenSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
        except:
            return Response(
                {"status": False, "message": "invalid  token"},
                status=status.HTTP_200_OK,
            )
        serializers = self.serializer_class(token)
        return Response(serializers.data, status=status.HTTP_200_OK)