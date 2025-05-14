from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import AllRequestsSerializer, RequestDetailSerializer, RequestUpdateSerializer, DonationDetailSerializer, DonationUpdateSerializer, InventorySerializer
from donor.serializers import AllDonationsSerializer
from .models import Worker, Inventory, Location, Status 
from patient.models import Request
from donor.models import Donation
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from user.models import Notification
# Create your views here.

class IsStaffUser(permissions.BasePermission):
    message = "Only staff members are allowed to access this resource."

    def has_permission(self, request, view):
        if not (request.user and request.user.is_staff):
            raise PermissionDenied(detail=self.message, code=status.HTTP_403_FORBIDDEN)
        return True

class InventoryView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating inventory details.
    Only accessible by staff users.
    """
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_object(self):
        try:
            return Inventory.objects.get(id=1) 
        except Inventory.DoesNotExist:
            raise NotFound(detail="Inventory not found", code=status.HTTP_404_NOT_FOUND)

class DonationListView(generics.ListAPIView):
    """
    API endpoint for retrieving all donations.
    Only accessible by staff users.
    """
    serializer_class = AllDonationsSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        return Donation.objects.all()

class DonationListByStatusView(generics.ListAPIView):
    """
    API endpoint for retrieving donations by status.
    Only accessible by staff users.
    """
    serializer_class = AllDonationsSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        status_param = self.kwargs.get('status')  # Get from URL, not query params
        valid_statuses = ['pending', 'scheduled', 'completed', 'cancelled']

        if status_param not in valid_statuses:
            return Donation.objects.none()

        return Donation.objects.filter(status__status=status_param)
    
class RequestListView(generics.ListAPIView):
    """
    API endpoint for retrieving all requests.
    Only accessible by staff users.
    """
    serializer_class = AllRequestsSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        return Request.objects.all()
class RequestListByStatusView(generics.ListAPIView):
    """
    API endpoint for retrieving requests by status.
    Only accessible by staff users.
    """
    serializer_class = AllRequestsSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        status_param = self.kwargs.get('status')  # Get from URL, not query params
        valid_statuses = ['pending', 'approved', 'fulfilled', 'declined']

        if status_param not in valid_statuses:
            return Request.objects.none()

        return Request.objects.filter(status__status=status_param)
    

class RequestDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Request.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return RequestUpdateSerializer
        return RequestDetailSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        inventory = Inventory.objects.first()  # Assuming there's only one inventory object

        # Check if the status is being updated to 'approved'
        if request.data.get('status') == 'approved':
            if inventory.units_available < instance.units_required:
                return Response(
                    {"detail": "Not enough units available in inventory to approve this request."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Deduct units from available and add to allocated
            inventory.units_available -= instance.units_required
            inventory.units_allocated += instance.units_required
            inventory.save()

        # Check if the status is being updated to 'fulfilled'
        if request.data.get('status') == 'fulfilled':
            inventory.units_allocated -= instance.units_required
            inventory.save()

        response = super().patch(request, *args, **kwargs)

        # Notify the patient about the status change
        instance.refresh_from_db()
        patient = instance.patient.user
        decline_reason = request.data.get('decline_reason', '').strip()

        if instance.status.status == 'pending':
            msg = f"Your request is waiting for approval. Please wait for further updates."
        elif instance.status.status == 'declined':
            msg = "Your blood request has been declined."
            if decline_reason:
                msg += f" Reason: {decline_reason}"
        elif instance.status.status == 'fulfilled':
            msg = "Your request has been fulfilled. Thank you for your patience!"
        elif instance.status.status == 'approved':
            msg = "Your request has been approved. You may receive blood from our locations."
        else:
            msg = f"Your request status has been updated to {instance.status.status}."

        Notification.objects.create(recipient=patient, message=msg)
        data = RequestDetailSerializer(instance).data
        return Response(data)

class DonationDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Donation.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return DonationUpdateSerializer
        return DonationDetailSerializer

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        instance = self.get_object()
        inventory = Inventory.objects.first()  # Assuming there's only one inventory object
        user = instance.donor.user
        cancel_reason = request.data.get('cancel_reason', '').strip()

        location_id = request.data.get('location')
        if location_id:
            try:
                location = Location.objects.get(pk=location_id)
                instance.location = location
                instance.save()
            except Location.DoesNotExist:
                return Response({"detail": "Invalid location ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the status is being updated to 'completed'
        if instance.status.status == 'completed':
            # Add the donated units to the inventory
            inventory.units_available += instance.units
            inventory.save()

        # Notify the donor about the status change
        if instance.status.status == 'pending':
            msg = f"Your donation is set to pending. Please wait for further updates."
        else:
            msg = f"Your donation status has been {instance.status.status}."
            if instance.status.status == 'completed':
                msg += f" Thank you for your contribution!"
            elif instance.status.status == 'scheduled':
                msg += f" You are advised to be at {instance.location} on {instance.date} at {instance.time}."
            elif instance.status.status == 'cancelled':
                if cancel_reason:
                    msg += f" Reason: {cancel_reason}"

        Notification.objects.create(recipient=user, message=msg)
        data = DonationDetailSerializer(instance).data
        return Response(data)
