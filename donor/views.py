from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from . models import Donor

# Register API
class RegisterAPI(generics.GenericAPIView):
    """
    API endpoint for donor registration.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        donor = serializer.save(user=request.user)

        return Response({
            "donor": donor.id,
            "message": "Donor registered successfully."
        }, status=status.HTTP_201_CREATED)