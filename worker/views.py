from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import AllRequestsSerializer
from donor.serializers import AllDonationsSerializer
from .models import Worker, Inventory, Location, Status 
from patient.models import Request
from donor.models import Donation
from rest_framework.views import APIView
# Create your views here.

class IsStaffUser(permissions.BasePermission):
    message = "Only staff members are allowed to access this resource."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class DonationListView(generics.ListAPIView):
    """
    API endpoint for retrieving all donations.
    Only accessible by staff users.
    """
    serializer_class = AllDonationsSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        return Donation.objects.all()
    
class RequestListByStatusView(generics.ListAPIView):
    """
    API endpoint for retrieving requests by status.
    Only accessible by staff users.
    """
    serializer_class = AllRequestsSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        valid_statuses = ['pending', 'approved', 'fulfilled', 'declined']

        if status_param not in valid_statuses:
            return Request.objects.none()  # Return empty queryset if invalid or no status given

        return Request.objects.filter(status__status=status_param).order_by('-request_date')

class DonationListByStatusView(generics.ListAPIView):
    """
    API endpoint for retrieving donations by status.
    Only accessible by staff users.
    """
    serializer_class = AllRequestsSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        valid_statuses = ['pending', 'scheduled', 'completed', 'cancelled']

        if status_param not in valid_statuses:
            return Request.objects.none()  # Return empty queryset if invalid or no status given

        return Request.objects.filter(status__status=status_param).order_by('-request_date')

# class PendingRequestListView(generics.ListAPIView):
#     """
#     API endpoint for retrieving pending requests.
#     """
#     serializer_class = AllRequestsSerializer
#     permission_classes = [permissions.IsAuthenticated, IsStaffUser]

#     def get_queryset(self):
#         return Request.objects.filter(status__status='pending').order_by('-request_date')

# class ApprovedRequestListView(generics.ListAPIView):
#     """
#     API endpoint for retrieving approved requests.
#     """
#     serializer_class = AllRequestsSerializer
#     permission_classes = [permissions.IsAuthenticated, IsStaffUser]

#     def get_queryset(self):
#         return Request.objects.filter(status__status='approved').order_by('-request_date')

# class FulfilledRequestListView(generics.ListAPIView):
#     """
#     API endpoint for retrieving fulfilled requests.
#     """
#     serializer_class = AllRequestsSerializer
#     permission_classes = [permissions.IsAuthenticated, IsStaffUser]

#     def get_queryset(self):
#         return Request.objects.filter(status__status='fulfilled').order_by('-request_date')

# class DeclinedRequestListView(generics.ListAPIView):
#     """
#     API endpoint for retrieving declined requests.
#     """
#     serializer_class = AllRequestsSerializer
#     permission_classes = [permissions.IsAuthenticated, IsStaffUser]

#     def get_queryset(self):
#         return Request.objects.filter(status__status='declined').order_by('-request_date')

