from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .serializers import RegisterSerializer, DonorSerializer, UpdateDonorSerializer, DonationSerializer, AllDonationsSerializer
from rest_framework.views import APIView
from . models import Donor
from worker.models import Status

# Register API
class RegisterAPI(generics.GenericAPIView):
    """
    API endpoint for donor registration.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if Donor.objects.filter(user=request.user).exists():
            return Response({
                "message": "Donor is already registered."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        donor = serializer.save(user=request.user)

        return Response({
            "donor": donor.id,
            "message": "Donor registered successfully."
        }, status=status.HTTP_201_CREATED)
    
# Donor API
class DonorAPI(generics.RetrieveAPIView):
    """
    API endpoint for retrieving donor details.
    """
    
    serializer_class = DonorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return Donor.objects.get(user=self.request.user)
        except Donor.DoesNotExist:
            raise NotFound(detail="Donor not found", code=status.HTTP_404_NOT_FOUND)
        
# Update Donor API
class UpdateDonorAPI(generics.UpdateAPIView):
    """
    API endpoint for updating donor details.
    """
    serializer_class = DonorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return Donor.objects.get(user=self.request.user)
        except Donor.DoesNotExist:
            raise NotFound(detail="Donor not found", code=status.HTTP_404_NOT_FOUND)
        
class PartialUpdateDonorAPI(APIView):
    """
    API endpoint for partially updating donor details.
    """
    serializer_class = UpdateDonorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        donor = Donor.objects.get(user=request.user)
        serializer = self.serializer_class(donor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DonationAPI(generics.CreateAPIView):
    """
    API endpoint for making a donation.
    """
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            donor = Donor.objects.get(user=request.user)
        except Donor.DoesNotExist:
            return Response({"message": "Register as donor first."}, status=status.HTTP_400_BAD_REQUEST)
        status_obj = Status.objects.get(pk=1)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(donor=donor, status=status_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DonationListAPI(generics.ListAPIView):
    """
    API endpoint for retrieving donations.
    """
    serializer_class = AllDonationsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            donations = self.request.user.donor.donations.all()
        except Donor.DoesNotExist:
            raise NotFound(detail="Donor not found", code=status.HTTP_404_NOT_FOUND)

        return donations