from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import AllRequestsSerializer
from .models import Worker, Inventory, Location, Status 
from patient.models import Request
from rest_framework.views import APIView
# Create your views here.

class ApprovedRequestListView(generics.ListAPIView):
    """
    API endpoint for retrieving approved requests.
    """
    serializer_class = AllRequestsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Request.objects.filter(status__status='approved').order_by('-request_date')