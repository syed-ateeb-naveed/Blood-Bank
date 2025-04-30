from rest_framework import serializers
from donor.models import Donation
from patient.models import Request


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
        fields = ('id', 'patient', 'blood_type', 'units_required', 'request_date')