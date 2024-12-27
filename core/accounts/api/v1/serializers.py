from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
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
        fields = ["username","email","password1","password2"]
        
    def validate(self,attrs):
        username = attrs.get("username")
        email = attrs.get('email')
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
                                        email= validated_data["email"],
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
    
    
    
class ChangePasswordSerialier(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "passswords doesnt match"})

        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return super().validate(attrs)


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "user does not exist"})
        if user_obj.is_staff:
            raise serializers.ValidationError(
                {"detail": "user is already activated "}
            )
        attrs["user"] = user_obj
        return super().validate(attrs)
    
"""class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        fields = ["email"]
    
    def validate(self, attrs):
        
        email = attrs["data"].get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(user.id)
            token = PasswordResetTokenGenerator().make_token(user)
          
                
        return super().validate(attrs)"""
        


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        write_only=True,
        error_messages={'invalid': ('Password must be at least 8 characters long with at least one capital letter and symbol')})
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    
