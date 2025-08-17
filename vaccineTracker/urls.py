from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VaccineViewSet, UserVaccineRecordViewSet, AdminVaccineViewSet, AdminUserVaccineRecordViewSet

router = DefaultRouter()
router.register(r"vaccines", VaccineViewSet, basename="vaccines")
router.register(r"vaccinations", UserVaccineRecordViewSet, basename="vaccinations")

router.register(r"admin/vaccines", AdminVaccineViewSet, basename="admin-vaccines")
router.register(r"admin/vaccinations", AdminUserVaccineRecordViewSet, basename="admin-vaccinations")

urlpatterns = [
    path("", include(router.urls)),
]
