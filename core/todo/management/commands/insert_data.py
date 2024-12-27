from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import datetime
from django.contrib.auth.models import User
from todo.models import Task



class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
    
        for i in range(5):
            Task.objects.create(
                user = User.objects.create(username=self.fake.user_name(), password="123456aA!"),
                title = self.fake.word(),
                description = self.fake.paragraph(nb_sentences=1),
                complete = random.choice([True, False]),
                created = datetime.now(),
            
            )