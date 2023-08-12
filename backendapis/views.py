from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, KeyValueSerializer
from .models import UserProfile, KeyValue
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator,
)
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.exceptions import NotFound

def home(request):
    return HttpResponse('Welcome to CRUD project using Django REST Framework. To test the apis, Please follow README file instructions!')


class UserRegistrationView(APIView):
    def post(self, request):
        try:
            if int(request.data.get('age')) <= 0:
                    error_response = {
                        "status": "error",
                        "code": "INVALID_AGE",
                        "message": "Invalid age value. Age must be a positive integer."
                    }
                    return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
            
            if request.data.get('gender') is None:
                    error_response = {
                        "status": "error",
                        "code": "GENDER_REQUIRED",
                        "message": "Gender field is required. Please specify the gender (e.g., male, female, non-binary)."
                    }
                    return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                if User.objects.filter(email=email).exists():
                    error_response = {
                        "status": "error",
                        "code": "EMAIL_EXISTS",
                        "message": "The provided email is already registered. Please use a different email address."
                    }
                    return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
                # Custom password validation
                password = serializer.validated_data.get('password')
                try:
                    MinimumLengthValidator().validate(password)
                    CommonPasswordValidator().validate(password)
                    NumericPasswordValidator().validate(password)
                    UserAttributeSimilarityValidator().validate(password)

                    # Custom validation for at least one uppercase and one lowercase letter
                    if not any(char.isupper() for char in password):
                        raise ValidationError("Password must contain at least one uppercase letter.")
                    if not any(char.islower() for char in password):
                        raise ValidationError("Password must contain at least one lowercase letter.")
                    
                except ValidationError as e:
                    error_response = {
                        "status": "error",
                        "code": "INVALID_PASSWORD",
                        "message": 'The provided password does not meet the requirements. Password must be at least 8 characters long and contain a mix of uppercase and lowercase letters, numbers, and special characters.'
                    }
                    return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

                user = serializer.save()
                response_data = {
                    "status": "success",
                    "message": "User successfully registered!",
                    "data": {
                        "user_id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "full_name": f"{user.first_name} {user.last_name}",
                        "age": user.userprofile.age,  
                        "gender": user.userprofile.gender
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                error_dict = serializer.errors
                if error_dict.get('username'):
                    error_code = error_dict['username'][0].code
                    if error_code == 'unique':
                        error_response = {
                            "status": "error",
                            "code": "USERNAME_EXISTS",
                            "message": "The provided username is already taken. Please choose a different username."
                        }
                        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
                    
                error_message = "Please provide all required fields listed here: "
                missing_fields = ', '.join(serializer.errors.keys())
                error_message += missing_fields + "."
                error_response = {
                    "status": "error",
                    "code": "INVALID_REQUEST",
                    "message": error_message
                }
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as ex:
            error_response = {
                "status": "error",
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred. Please try again later."
            }
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            access_token = response.data.get("access_token")
            expires_in = response.data.get("expires_in")
            formatted_response = {
                "status": "success",
                "message": "Access token generated successfully.",
                "data": {
                    "access_token": access_token,
                    "expires_in": expires_in,
                },
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            error_code = e.detail.get("error_code", None)
            if error_code == "MISSING_FIELDS":
                error_message = "Missing fields. Please provide both username and password."
            elif error_code == 'INVALID_CREDENTIALS':
                error_message = "Invalid credentials. The provided username or password is incorrect."
            else:
                error_code = "INTERNAL_ERROR"
                error_message = "Internal server error occurred. Please try again later."
            return Response(
                {
                    "status": "error",
                    "error_code": error_code,
                    "message": error_message,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # Handle other unexpected exceptions here
            error_code = "INTERNAL_ERROR"
            error_message = "Internal server error occurred. Please try again later."

            return Response(
                {
                    "status": "error",
                    "error_code": error_code,
                    "message": error_message,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
class KeyValueListCreateView(generics.ListCreateAPIView):
    queryset = KeyValue.objects.all()
    serializer_class = KeyValueSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            "status": "success",
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        key = request.data.get('key')
        value = request.data.get('value')

        if not key:
            response_data = {
                "status": "error",
                "error_code": "INVALID_KEY",
                "message": "The provided key is not valid or missing."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if not value:
            response_data = {
                "status": "error",
                "error_code": "INVALID_VALUE",
                "message": "The provided value is not valid or missing."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Check if key already exists
        if KeyValue.objects.filter(key=key).exists():
            response_data = {
                "status": "error",
                "error_code": "KEY_EXISTS",
                "message": "The provided key already exists in the database. To update an existing key, use the update API."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = {
            "status": "success",
            "message": "Data stored successfully."
        }

        return Response(response_data, status=status.HTTP_200_OK)

class KeyValueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KeyValue.objects.all()
    serializer_class = KeyValueSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'key'  # Specify the field to use for looking up instances
    

    def get_object(self):
        key = self.kwargs.get(self.lookup_field)
        try:
            return KeyValue.objects.get(key=key)
        except KeyValue.DoesNotExist:
            response_data = {
                "status": "error",
                "error_code": "KEY_NOT_FOUND",
                "message": "The provided key does not exist in the database."
            }
            raise NotFound(detail=response_data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response_data = {
            "status": "success",
            "data": {
                "key": instance.key,
                "value": instance.value
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_data = {
            "status": "success",
            "message": "Data updated successfully."
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        response_data = {
            "status": "success",
            "message": "Data deleted successfully."
        }

        return Response(response_data, status=status.HTTP_200_OK)

