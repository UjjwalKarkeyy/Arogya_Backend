from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, FAQViewSet

router = DefaultRouter()
router.register(r'chat', ChatViewSet, basename="chat")
router.register(r'faq', FAQViewSet, basename="faq")
router.register(r'faq/categories', FAQViewSet, basename="faqCategories")

urlpatterns = router.urls