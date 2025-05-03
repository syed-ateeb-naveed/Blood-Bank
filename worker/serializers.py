from rest_framework import serializers
from donor.models import Donation
from patient.models import Request
from donor.serializers import DonorSerializer
from patient.serializers import PatientSerializer
from .models import Status


class StatusField(serializers.PrimaryKeyRelatedField):
    """
    Custom field to handle status as a string instead of an object.
    """
    # def to_representation(self, value):
    #     return value.status if value else None

    # def to_internal_value(self, data):
    #     try:
    #         return Status.objects.get(status=data)
    #     except Status.DoesNotExist:
    #         raise serializers.ValidationError(f"Status '{data}' does not exist.")
    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                return Status.objects.get(status=data)
            except Status.DoesNotExist:
                raise serializers.ValidationError(f"Status '{data}' not found.")
        return super().to_internal_value(data)

class RequestDetailSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    status = serializers.CharField(source='status.status', read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'patient', 'blood_type', 'units_required', 'request_date', 'status']


class RequestUpdateSerializer(serializers.ModelSerializer):
    status = StatusField(queryset=Status.objects.all())
    decline_reason = serializers.CharField(write_only=True, required=False, allow_blank=True)
    class Meta:
        model = Request
        fields = ['status', 'decline_reason']  # Allow status update only


class DonationDetailSerializer(serializers.ModelSerializer):
    donor = DonorSerializer(read_only=True)
    status = serializers.CharField(source='status.status', read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'donor', 'units', 'date', 'time', 'location', 'status']


class DonationUpdateSerializer(serializers.ModelSerializer):
    status = StatusField(queryset=Status.objects.all())
    class Meta:
        model = Donation
        fields = ['status', 'date']  # Allow update of status and date

class AllDonationsSerializer(serializers.ModelSerializer):
    """
    Serializer for all donations
    """
    status = serializers.CharField(source='status.status')

    class Meta:
        model = Donation
        fields = ('id', 'donor', 'blood_type', 'units_donated', 'donation_date', 'location')
    
class AllRequestsSerializer(serializers.ModelSerializer):
    """
    Serializer for all requests
    """
    status = serializers.CharField(source='status.status')

    class Meta:
        model = Request
        fields = ('id', 'patient', 'blood_type', 'units_required', 'request_date', 'status')