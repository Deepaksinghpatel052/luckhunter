from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import api_views

app_name = 'accounts_api'

urlpatterns = [
    path('register/', api_views.RegisterAPIView.as_view(), name='register'),
    path('login/', api_views.EmailTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', api_views.MeAPIView.as_view(), name='me'),
]
