from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view
from .models import Tip
from .serializers import TipSerializer, TipCreateSerializer

# Optional django-filter support (kept exactly like your original)
try:
    from django_filters.rest_framework import DjangoFilterBackend
    import django_filters
    HAS_DJANGO_FILTER = True

    class TipFilter(django_filters.FilterSet):
        """Filter for tips"""
        title = django_filters.CharFilter(lookup_expr='icontains')
        content = django_filters.CharFilter(lookup_expr='icontains')
        is_active = django_filters.BooleanFilter()

        class Meta:
            model = Tip
            fields = ['title', 'content', 'is_active']

except ImportError:
    HAS_DJANGO_FILTER = False
    DjangoFilterBackend = None
    TipFilter = None


# Build filter_backends list the same way you did before
_FILTER_BACKENDS = [SearchFilter, OrderingFilter]
if HAS_DJANGO_FILTER and DjangoFilterBackend:
    _FILTER_BACKENDS.insert(0, DjangoFilterBackend)


class TipViewSet(viewsets.ModelViewSet):
    """
    Endpoints (unchanged URIs when registered as 'tips'):
    - GET  /api/tips/         -> list active tips (is_active=True)
    - POST /api/tips/         -> create a new tip (uses TipCreateSerializer)
    - GET  /api/tips/{id}/    -> retrieve any tip
    - PUT  /api/tips/{id}/    -> update (uses TipCreateSerializer for input)
    - PATCH /api/tips/{id}/   -> partial update (same as above)
    - DELETE /api/tips/{id}/  -> delete
    """
    serializer_class = TipSerializer  # default for read
    filter_backends = _FILTER_BACKENDS
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    filterset_class = TipFilter if HAS_DJANGO_FILTER else None

    def get_queryset(self):
        # Preserve: list -> only active; detail/update/delete -> all
        if getattr(self, 'action', None) == 'list':
            return Tip.objects.filter(is_active=True)
        return Tip.objects.all()

    def get_serializer_class(self):
        # Preserve: write with TipCreateSerializer, read with TipSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return TipCreateSerializer
        return TipSerializer

    # Preserve: return full read serializer on create/update
    def create(self, request, *args, **kwargs):
        write_ser = self.get_serializer(data=request.data)
        write_ser.is_valid(raise_exception=True)
        tip = write_ser.save()
        read_ser = TipSerializer(tip)
        headers = self.get_success_headers(read_ser.data)
        return Response(read_ser.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        write_ser = self.get_serializer(instance, data=request.data, partial=partial)
        write_ser.is_valid(raise_exception=True)
        tip = write_ser.save()
        read_ser = TipSerializer(tip)
        return Response(read_ser.data)


@api_view(['GET'])
def health_stats(request):
    """
    Get health statistics
    GET /api/stats/
    """
    total_tips = Tip.objects.filter(is_active=True).count()
    return Response({'total_tips': total_tips})
