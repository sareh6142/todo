from django.shortcuts import render
from .tasks import sendEmail
from django.http import HttpResponse, JsonResponse
from django_celery_beat.models import PeriodicTask


# Create your views here.
def send_email(request):
    sendEmail.delay()
    return HttpResponse("<h1>Done Sending</h1>")


def clean():
    Task = PeriodicTask.objects.all()
    for task in Task:
        if task.totol_run_count != 0:
            task.delete()