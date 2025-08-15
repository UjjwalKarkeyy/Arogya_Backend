from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipViewSet

router = DefaultRouter()
router.register(r'tips', TipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]