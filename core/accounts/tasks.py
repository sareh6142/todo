from celery import shared_task
from time import sleep

#from django_celery_beat.models import PeriodicTask

def import_django_instance():
    """
    Makes django environment available 
    to tasks!!
    """
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()



@shared_task
def sendEmail():
    sleep(2)
    print("done sending email")
    

@shared_task
def clean():
    import_django_instance()
    from django_celery_beat.models import PeriodicTask

    Task = PeriodicTask.objects.all()
    for task in Task:
        if task.total_run_count != 0:
            #id = task.id
            #revoke(id, terminate=True, signal="KILL")
            task.delete()
            
           
   