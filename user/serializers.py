from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

User = get_user_model()

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details
    """

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'pic','date_of_birth', 
            'age', 'is_active', 'is_staff'
        )

# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration, handles password creation.
    """
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=True)
    pic = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'date_of_birth', 'pic')
    
    def create(self, validated_data):
        """
        Create a new user with the provided email and password.
        Password is hashed using the create_user method.
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
            date_of_birth=validated_data['date_of_birth'],
            pic=validated_data.get('pic', None)
        )
        return user

# Serializer for user login
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login credentials validation.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validate login credentials and authenticate the user.
        """
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # Authenticate the user
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if user:
                if user.is_active:
                    return user
                raise serializers.ValidationError("User account is not active.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
