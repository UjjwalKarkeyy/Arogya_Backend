# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from complainFeedback.views import ComplainViewSet, ComplaintCommentViewSet

router = DefaultRouter()
router.register(r'complains', ComplainViewSet)
router.register(r'comments', ComplaintCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Removed 'api/'
]
