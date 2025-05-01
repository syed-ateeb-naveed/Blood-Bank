from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db import transaction
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, NotificationSerializer
from .models import Notification


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

class UserNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        # Get the queryset first
        queryset = self.get_queryset()

        # Mark all unread notifications as read
        queryset.filter(is_read=False).update(is_read=True)

        # Now call the original list() to return response
        return super().list(request, *args, **kwargs)

class UserNotificationCount(generics.GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        count = Notification.objects.filter(recipient=self.request.user, is_read=False).count()
        return Response({"unread_count": count}, status=status.HTTP_200_OK)