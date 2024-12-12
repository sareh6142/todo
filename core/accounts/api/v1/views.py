from rest_framework import generics
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.password_validation import validate_password


class RegistrationApiView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer
    
    def post(self,request,*args,**kwargs):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "username" : serializer.validated_data["username"]
                
            }
            return Response(data,status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)