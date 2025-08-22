from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SignupSerializer, LoginSerializer, PatientSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Patient

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message":"User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'message':'Login Successful',
                'token':{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class DefaultPatientView(APIView):
    def get(self, request):
        """
        Returns a default patient or creates one if none exists
        """
        try:
            # Try to get the first patient or create a default one
            patient = Patient.objects.first()
            
            if not patient:
                # Create a default user and patient if none exists
                default_user, created = User.objects.get_or_create(
                    username='default_patient',
                    defaults={
                        'email': 'default@patient.com',
                        'first_name': 'Default',
                        'last_name': 'Patient'
                    }
                )
                
                patient, created = Patient.objects.get_or_create(
                    user=default_user,
                    defaults={
                        'phone_number': '+1234567890',
                        'address': 'Default Address',
                        'blood_group': 'O+',
                        'medical_history': 'No significant medical history'
                    }
                )
            
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve default patient: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )