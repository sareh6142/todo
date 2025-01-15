
from celery import shared_task
from time import sleep
from django_celery_beat.models import PeriodicTask


@shared_task
def sendEmail():
    sleep(3)
    print("done sending email")
    

@shared_task
def clean():
    pass
"""    Task = PeriodicTask.objects.all()
    for task in Task:
        if task.totol_run_count != 0:
            task.delete()
           
   """