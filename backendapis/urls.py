from django.urls import path, include
from .views import UserRegistrationView, CustomTokenObtainPairView
from rest_framework.routers import DefaultRouter
from .views import KeyValueListCreateView, KeyValueDetailView, CustomTokenObtainPairView, home
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'), #To register a new user
    path('api/token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'), #create a user token to authenticate user to access apis
    path('api/data/', KeyValueListCreateView.as_view(), name='list-key-value'), #GET: list all the key pair, POST: to create a new record
    path('api/data/<str:key>/', KeyValueDetailView.as_view(), name='key-value-detail'), #Handling GET,PUT and DELETE operations

]