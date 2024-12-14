from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password1 = serializers.CharField(
        label="Password1",
        style={"input_type": "password1"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )
    password2 = serializers.CharField(
        label="Password2",
        style={"input_type": "password2"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )
    
    class Meta:
        model = User
        fields = ["username","password1","password2"]
        
    def validate(self,attrs):
        username = attrs.get("username")
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        if password1 != password2:
            raise serializers.ValidationError({"detail":"password does not match"})
        
        try:
            validate_password(attrs.get("password1"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password":list(e.messages)})
        
        
        if User.objects.filter(username=username).exists():
            msg = "User already exists pick another username"
            raise serializers.ValidationError({"user":msg})
            
        return super().validate(attrs)
    
    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password1'])
        
    
    
class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="username", write_only=True)
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label="Token", read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError({"details": "user is not verified"})
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "user is not verified"})
        validated_data["username"] = self.user.username
        validated_data["user_id"] = self.user.id
        return validated_data