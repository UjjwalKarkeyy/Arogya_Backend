from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Doctor, Specialty
from .serializers import DoctorSerializer, SpecialtySerializer


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /doctors/            -> list (with ?search=&specialty=)
    GET /doctors/{id}/       -> retrieve (optional extra vs. your original)
    """
    serializer_class = DoctorSerializer

    def get_queryset(self):
        queryset = Doctor.objects.filter(is_available=True)

        search = self.request.query_params.get('search')
        specialty = self.request.query_params.get('specialty')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(specialty__name__icontains=search)
            )

        if specialty and specialty != 'All':
            try:
                specialty_id = int(specialty)
                queryset = queryset.filter(specialty_id=specialty_id)
            except (ValueError, TypeError):
                queryset = queryset.filter(specialty__name__icontains=specialty)

        return queryset

    def list(self, request, *args, **kwargs):
        # use DRF's filter_queryset to play nicely with future filter backends/pagination
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': {
                'doctors': serializer.data,
                'total': len(serializer.data)
            }
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': {
                'doctor': serializer.data
            }
        })


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /specialties/        -> list
    GET /specialties/{id}/   -> retrieve (optional extra vs. your original)
    """
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': {
                'specialties': serializer.data,
                'total': len(serializer.data)
            }
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': {
                'specialty': serializer.data
            }
        })


class SystemViewSet(viewsets.ViewSet):
    """
    Exposes a health check endpoint as a ViewSet action.
    Registered as 'system', it will be available at: GET /system/health-check/
    """
    @action(detail=False, methods=['get'], url_path='health-check')
    def health_check(self, request):
        return Response({
            'success': True,
            'message': 'Django Doctor Directory API is running',
            'status': 'healthy'
        })
