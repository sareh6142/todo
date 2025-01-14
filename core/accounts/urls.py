from django.urls import path,include
from . import views

app_name = "accounts"


urlpatterns = [
    #path('',include('accounts.contrib.auth.urls')),
    path('api/v1/',include('accounts.api.v1.urls')),
    path("send-email/", views.send_email, name="send-email"),

]
