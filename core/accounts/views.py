from django.shortcuts import render
from .tasks import sendEmail
from django.http import HttpResponse, JsonResponse


# Create your views here.
def send_email(request):
    sendEmail.delay()
    return HttpResponse("<h1>Done Sending</h1>")