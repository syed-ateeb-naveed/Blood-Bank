from rest_framework import serializers
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from . models import Request, Patient
from user.serializers import UserSerializer

# Serializer for Donor model
class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for patient details
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ('id', 'user')
    
class RequestSerializer(serializers.ModelSerializer):
    """
    Serializer for donation details
    """
    patient = PatientSerializer(read_only=True)
    status = serializers.CharField(source='status.status', read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'patient', 'blood_type', 'units_required', 'request_date', 'status')

class AllRequestsSerializer(serializers.ModelSerializer):
    """
    Serializer for all donations
    """
    status = serializers.CharField(source='status.status')
    
    class Meta:
        model = Request
        fields = ('id', 'patient', 'blood_type', 'units_required', 'request_date', 'status')