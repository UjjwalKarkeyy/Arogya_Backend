from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LabReportViewSet, LabTestViewSet, HospitalViewSet

router = DefaultRouter()
router.register(r'lab-tests', LabTestViewSet, basename='labtest')
router.register(r'hospitals', HospitalViewSet, basename='hospital')
router.register(r'reports', LabReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]