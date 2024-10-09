from rest_framework import serializers
from .models import User


class UserPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']


class VerifyNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_code = serializers.CharField(max_length=6)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'profile_photo', 'phone_number', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'phone_number', 'profile_photo', 'role',]


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, help_text='Refresh token to be blacklisted.')
