from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import User
from django_session_jwt.middleware.session import SessionMiddleware
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError

from uuid import getnode as get_mac
from rest_framework import status
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(max_length=2000, min_length=3, read_only=True)
    class Meta:
        model = User
        fields = ["email", "username", "password", "phone","token",'kind']

    def validate(self, attrs):
        email = attrs.get("email", "")
        return attrs

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        validated_data["token"] = token.key
        return validated_data

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=5555555555555555555)

    class Meta:
        model = User
        fields = ["token"]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=2000, min_length=3, read_only=True)
    token = serializers.CharField(max_length=2000, min_length=3, read_only=True)
    kind = serializers.CharField(max_length=2000, min_length=3, read_only=True)
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "username",
            "id",
            'token',
            'kind'
        ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        try:
            user = auth.authenticate(email=email, password=password)
            if not user:
                if not User.objects.filter(email=email).exists():
                    return {
                    "email": "your email is incorrect",
                    "username": "user.username",
                }
                return {
                    "email": " كلمة السر خاطئة",
                    "username": "user.username",
                }
           
                
            tt, token = Token.objects.get_or_create(user=user)
            return {
                "email": user.email,
                "username": user.username,
                "token": tt.key,
                'kind':user.kind
            }
            return super().validate(attrs)

        except Exception as e:
            raise serializers.ValidationError(str(e))



class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")

class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['kind','phone','is_staff','email']

class TokenSerializers(serializers.ModelSerializer):
    user= UserSer(read_only=True)
    class Meta:
        model = Token
        fields= ['user']
