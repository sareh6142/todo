from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

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