from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from .serializers import UserRegisterSerializer

from utils.response import (
    response_400_bad_request,
    response_200,
)

from .utils import (
    send_verification_email,
)
class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]  # Anyone can register

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user, request)
            return response_200('User created successfully!', serializer.data)
            
        return response_400_bad_request(serializer.errors)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                data = {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }
                return response_200('User logged in successfully!', data)
            else:
                return response_400_bad_request('Invalid Credentials')
        except User.DoesNotExist:
            return response_400_bad_request('Invalid Credentials')