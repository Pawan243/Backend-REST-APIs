from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, KeyValue
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(write_only=True)
    gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'age', 'gender')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'age': {'required': True},
            'gender': {'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        profile_data = {
            'age': validated_data.pop('age'),
            'gender': validated_data.pop('gender')
        }
        user = User.objects.create(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def run_validation(self, data=None):
        if not data or not data.get("username") or not data.get("password"):
            raise AuthenticationFailed(detail={"error_code": "MISSING_FIELDS"})

        return super().run_validation(data)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username, password=password)
        print(user, username, password)
        if len(user) == 0:
            superuser = authenticate(username=username, password=password)
            if superuser is None:
                raise AuthenticationFailed(detail={"error_code": "INVALID_CREDENTIALS"})
            else:
                refresh = self.get_token(superuser)
                data = {
                    "access_token": str(refresh.access_token),
                    "expires_in": 3600,
                }
                return data
        else:
            refresh = self.get_token(user[0])
            data = {
                "access_token": str(refresh.access_token),
                "expires_in": 3600,
            }
            return data

    def user_exists(self, username):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=username)
            return user
        except user_model.DoesNotExist:
            return None
        


# serializers.py
from rest_framework import serializers
from .models import KeyValue

class KeyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyValue
        fields = ('key', 'value')










# from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.exceptions import AuthenticationFailed
# from django.contrib.auth import get_user_model

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         username = attrs.get("username")
#         password = attrs.get("password")

#         if not username or not password:
#             raise AuthenticationFailed("MISSING_FIELDS")

#         user = self.user_exists(username)
#         if user is None or not user.check_password(password):
#             raise AuthenticationFailed("INVALID_CREDENTIALS")

#         refresh = self.get_token(user)
#         data = {
#             "access_token": str(refresh.access_token),
#             "expires_in": 3600,
#         }

#         return data

#     def user_exists(self, username):
#         user_model = get_user_model()
#         try:
#             user = user_model.objects.get(username=username)
#             return user
#         except user_model.DoesNotExist:
#             return None




