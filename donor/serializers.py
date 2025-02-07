from rest_framework import serializers
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from . models import Donor


# Serializer for User model
# class UserSerializer(serializers.ModelSerializer):
#     """
#     Serializer for donor details
#     """

#     class Meta:
#         model = Donor
#         fields = (
#             'user', 'email', 'first_name', 'last_name', 'pic','date_of_birth', 
#             'age', 'blood_group', 'is_active', 'is_staff'
#         )

# Serializer for user registration
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