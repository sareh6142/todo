from django.urls import path, include
from . import views
#from rest_framework.authtoken.views import ObtainAuthToken

app_name = "api-v1"

urlpatterns = [
        path("register/", views.RegistrationApiView.as_view(), name="register"),
        path("token/login",views.ObtainAuthToken.as_view(),name = "token-login"),
        path("token/logout/",views.CustomDiscardAuthToken.as_view(),name="token-logout",
    ),

]