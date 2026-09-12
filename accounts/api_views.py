from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import LsUser
from .serializear import (
    EmailTokenObtainPairSerializer,
    LsUserProfileSerializer,
    RegisterSerializer,
)


class RegisterAPIView(generics.CreateAPIView):
    """
    Create a new account (User + LsUser profile). Username is set to
    the given email, matching how the existing website logs users in.

    Public endpoint: no authentication required.
    """

    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ls_user = serializer.save()
        return Response(
            {
                'message': 'Registration successful. You can now log in.',
                'email': ls_user.user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Log in with email + password, receive a JWT access/refresh token
    pair. Send the access token as `Authorization: Bearer <access>` on
    subsequent authenticated requests.

    Public endpoint: no authentication required.
    """

    serializer_class = EmailTokenObtainPairSerializer


class MeAPIView(generics.RetrieveAPIView):
    """
    Return the signed-in user's own profile.

    Requires authentication: send a valid JWT access token as
    `Authorization: Bearer <access>`.
    """

    serializer_class = LsUserProfileSerializer

    def get_object(self):
        return LsUser.objects.get(user=self.request.user)
