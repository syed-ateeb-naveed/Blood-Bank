from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db import transaction
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer


User = get_user_model()

# Register API
class RegisterAPI(generics.GenericAPIView):
    """
    API endpoint for user registration.
    Handles user creation, initializes the user's wallet, and provides a refresh and access token upon successful registration.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": {
                'refresh': str(refresh),
                'access': access,
            }
        })

# Login API
class LoginAPI(TokenObtainPairView):
    """
    API endpoint for user login.
    Provides a refresh and access token upon successful login.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": {
                'refresh': str(refresh),
                'access': access,
            }
        })

# Get User API
class UserAPI(generics.RetrieveAPIView):
    """
    API endpoint for retrieving the currently authenticated user's details.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
