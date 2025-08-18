
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet

router = DefaultRouter()
router.register(r'', NewsViewSet)  # This makes the endpoint /news/

urlpatterns = router.urls