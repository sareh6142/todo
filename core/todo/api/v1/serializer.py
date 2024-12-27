from rest_framework import serializers
from ...models import Task
from django.contrib.auth.models import User


<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
\
>>>>>>> Stashed changes
=======
\
>>>>>>> Stashed changes

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =  "__all__"



class TaskSerializer(serializers.ModelSerializer):
    username1 = serializers.SerializerMethodField()
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    
    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "username1",
            "title",
            "description",
            "complete",
            "created",
            "relative_url",
            
          
        ]
        read_only_fields = ["user"]
        

              
                
    def get_username1(self,obj):
        return str(obj.user.username)
    
    def create(self, validated_data):
        validated_data["user"] = User.objects.get(
            id=self.context.get("request").user.id
        )
        return super().create(validated_data)
    
    
        

        
       