from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

#from rest_framework.authtoken.views import ObtainAuthToken

app_name = "api-v1"

urlpatterns = [
        path("register/", views.RegistrationApiView.as_view(), name="register"),
        path("token/login",views.ObtainAuthToken.as_view(),name = "token-login"),
        path("token/logout/",views.CustomDiscardAuthToken.as_view(),name="token-logout"),
             
        
        path("jwt/create/",views.TokenObtainPairView.as_view(),name="jwt-create"),
        path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
        path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
        
        path("change-password/",views.ChangePasswordApiView.as_view(),name="change-password"),
        
        #path("", views.ProfileApiView.as_view(), name="profile"),
    

]