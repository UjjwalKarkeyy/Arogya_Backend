from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipViewSet, health_stats

router = DefaultRouter()
router.register(r'tips', TipViewSet, basename='tips')

urlpatterns = [
    path('', include(router.urls)),     # /api/tips/, /api/tips/{id}/
    path('stats/', health_stats),       # /api/stats/ (unchanged)
]
