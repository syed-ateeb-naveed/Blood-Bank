from rest_framework import serializers
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from . models import Donor, Donation, Location
from user.serializers import UserSerializer

# Serializer for Donor model

class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for location details
    """
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'type', 'link')
class DonorSerializer(serializers.ModelSerializer):
    """
    Serializer for donor details
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Donor
        fields = ('id', 'user', 'blood_group', 'gender', 'height', 'weight', 'ailments')

#Serializer for donor edit

class UpdateDonorSerializer(serializers.ModelSerializer):
    """
    Serializer for updating donor details
    """
    class Meta:
        model = Donor
        fields = ('blood_group', 'gender', 'height', 'weight', 'ailments') 
        
# Serializer for donor registration
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration, handles password creation.
    """
    blood_group = serializers.CharField(write_only=True, required=True)
    gender = serializers.CharField(required=True)
    height = serializers.FloatField(required=True)
    weight = serializers.FloatField(required=True)
    ailments = serializers.CharField(required=False)

    class Meta:
        model = Donor
        fields = ('id', 'user', 'blood_group', 'gender', 'height', 'weight', 'ailments')
        extra_kwargs = {
            'user': {'read_only': True} 
        }
    
    def create(self, validated_data):
        """
        Create a new donor
        """
        donor = Donor.objects.create(
            user=self.context['request'].user,
            blood_group = validated_data['blood_group'],
            gender = validated_data['gender'],
            height = validated_data['height'],
            weight = validated_data['weight'],
            ailments=validated_data.get('ailments', '')
        )

        return donor
    
class DonationSerializer(serializers.ModelSerializer):
    """
    Serializer for donation details
    """
    donor = DonorSerializer(read_only=True)
    status = serializers.CharField(source='status.status', read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = ('id', 'donor', 'date', 'time', 'units', 'location', 'status')

class AllDonationsSerializer(serializers.ModelSerializer):
    """
    Serializer for all donations
    """
    status = serializers.CharField(source='status.status')
    location = LocationSerializer(read_only=True)
    class Meta:
        model = Donation
        fields = ('id', 'donor', 'date', 'time', 'units', 'location', 'status')