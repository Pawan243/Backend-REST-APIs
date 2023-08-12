from django.urls import path, include
from .views import UserRegistrationView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import CustomTokenObtainPairView

from rest_framework.routers import DefaultRouter
from .views import KeyValueListCreateView, KeyValueDetailView

# router = DefaultRouter()
# router.register(r'', KeyValueViewSet)


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    # path('data/',include(router.urls))
    path('data/', KeyValueListCreateView.as_view(), name='list-key-value'), #GET: list all the key pair, POST: to create a new record
    path('data/<str:key>/', KeyValueDetailView.as_view(), name='key-value-detail'), #Handling GET,PUT and DELETE operations

]