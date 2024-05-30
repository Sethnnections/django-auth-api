from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from users_auth.serializers import (
    RegistrationSerializer,
    UserSerializer,
    ProfileSerializer,
)

from users_auth.models import CustomUser, Profile


class UserRegistration(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile = Profile.objects.create(user=user)  # Create a profile for the user
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = CustomUser.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            profile = user.profile  # Try to get the profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(
                user=user
            )  # Create the profile if it doesn't exist
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateProfileSerializer(request.user.profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
