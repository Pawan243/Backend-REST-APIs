from django.urls import path, include
from .views import UserRegistrationView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import CustomTokenObtainPairView

from rest_framework.routers import DefaultRouter
from .views import KeyValueViewSet

router = DefaultRouter()
router.register(r'', KeyValueViewSet)


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('data/',include(router.urls))
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]