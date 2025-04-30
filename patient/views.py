from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .serializers import RequestSerializer, AllRequestsSerializer
from rest_framework.views import APIView
from . models import Patient, Request
from worker.models import Status

        
class RequestAPI(generics.CreateAPIView):
    """
    API endpoint for making a donation.
    """
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            patient = Patient.objects.create(user=request.user)
        status_obj = Status.objects.get(status='pending')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(patient=patient, status=status_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RequestListAPI(generics.ListAPIView):
    """
    API endpoint for retrieving donations.
    """
    serializer_class = AllRequestsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            patient = Patient.objects.get(user=self.request.user)
            requests = patient.requests.all()
        except Patient.DoesNotExist:
            raise NotFound({"detail": "You have not made any blood requests"}, code=status.HTTP_404_NOT_FOUND)

        return requests