from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Patient

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['username','email','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email = validated_data['email'],
            password= validated_data['password'],
        )

        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username = data['username'],
            password = data['password'],
        )

        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        
        return user

class PatientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'date_of_birth', 'address', 'emergency_contact',
            'blood_group', 'medical_history', 'created_at', 'updated_at'
        ]