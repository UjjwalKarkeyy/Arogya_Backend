# doctor/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, SpecialtyViewSet, SystemViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')          # ← add basename
router.register(r'specialties', SpecialtyViewSet, basename='specialty')# ← safe even though it has queryset
router.register(r'system', SystemViewSet, basename='system')           # ← required (no queryset)

urlpatterns = [
    path('', include(router.urls)),
]
