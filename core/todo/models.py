from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_api_url(self):

        return reverse("todo:api-v1:task-detail", kwargs={"pk": self.pk})


    class Meta:
        ordering = ['complete']
        
