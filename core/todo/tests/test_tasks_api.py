from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from todo.models import Task
from datetime import datetime
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create(
        username="jamshid", password="123456aA!",is_superuser = True,
    )
    return user

@pytest.mark.django_db
class TestTaskApi:
    
    def test_get1_Task_response_200_status(self,api_client):
        
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 200
        
        
    def test_post4_Task_response_201_user_status(self,api_client,common_user):
        url = reverse("todo:api-v1:task-list")        
        data = {
                "title" : "salam3",
                "description" : "salam3",
                "complete" : True,
                "created" : datetime.now(),
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url,data)
        assert response.status_code == 201
        
    def test_get2_Task_response_200_status(self,api_client):
        
        url2 = reverse("todo:api-v1:task-detail", kwargs = {"pk": 1})
        response = api_client.get(url2)
        assert response.status_code == 200
        
    def test_post3_Task_response_401_status(self,api_client):
        
        url = reverse("todo:api-v1:task-list")
        data = {
                "title" : "salam2",
                "description" : "salam2",
                "complete" : True,
                "created" : datetime.now(),
        }
        response = api_client.post(url,data)
        assert response.status_code == 401
        
    
        
    def test_post5_Task_response_invalid_data_status(self,api_client,common_user):
        url = reverse("todo:api-v1:task-list")
        data = {
                "title" : "salam5",
                "description" : "salam5",
                
               
        }
        user = common_user
        api_client.force_login(user=user)
        response = api_client.post(url,data)
        assert response.status_code == 201