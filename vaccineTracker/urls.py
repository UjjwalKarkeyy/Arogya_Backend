from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VaccineViewSet, UserVaccineRecordViewSet

router = DefaultRouter()
router.register(r"vaccines", VaccineViewSet, basename="vaccines")
router.register(r"vaccinations", UserVaccineRecordViewSet, basename="vaccinations")

urlpatterns = [
    path("", include(router.urls)),
]
