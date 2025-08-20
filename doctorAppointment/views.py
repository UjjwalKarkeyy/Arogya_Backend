from datetime import datetime
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer

class AppointmentViewSet(viewsets.GenericViewSet):
    """
    Endpoints
    ---------
    GET  /appointments/                                  -> list
    POST /appointments/                                  -> create
    GET  /appointments/available-slots/?doctor_id=&date= -> available slots
    """
    queryset = Appointment.objects.all()

    def get_serializer_class(self):
        # Use write serializer on POST; read serializer otherwise
        return (
            AppointmentCreateSerializer
            if self.request and self.request.method == 'POST'
            else AppointmentSerializer
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()
            response_serializer = AppointmentSerializer(
                appointment, context=self.get_serializer_context()
            )
            return Response({
                'success': True,
                'message': 'Appointment booked successfully!',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Failed to book appointment',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='available-slots')
    def available_slots(self, request):
        """
        GET /appointments/available-slots/?doctor_id=1&date=YYYY-MM-DD
        """
        doctor_id = request.query_params.get('doctor_id')
        date_str = request.query_params.get('date')

        if not doctor_id:
            return Response({
                'success': False,
                'message': 'doctor_id parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not date_str:
            return Response({
                'success': False,
                'message': 'date parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                'success': False,
                'message': 'Invalid date format. Use YYYY-MM-DD'
            }, status=status.HTTP_400_BAD_REQUEST)

        # All defined time slots on the model
        all_slots = [slot[0] for slot in Appointment.TIME_SLOTS]

        # Slots already booked for this doctor on this date
        booked_slots = Appointment.objects.filter(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            status__in=['pending', 'confirmed']
        ).values_list('appointment_time', flat=True)

        # Remaining slots
        remaining = [s for s in all_slots if s not in booked_slots]

        formatted = [{'value': s, 'label': dict(Appointment.TIME_SLOTS)[s]} for s in remaining]

        return Response({
            'success': True,
            'data': {
                'date': date_str,
                'available_slots': formatted
            }
        })
