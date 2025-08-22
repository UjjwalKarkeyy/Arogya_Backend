from django.urls import path
from .views import SignupView, LoginView, DefaultPatientView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/default-patient/', DefaultPatientView.as_view(), name='default-patient'),
]

