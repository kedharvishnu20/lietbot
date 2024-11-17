import json
from django.core.management.base import BaseCommand
from chatbot.models import FAQ

class Command(BaseCommand):
    help = "Load dataset into the database"

    def handle(self, *args, **kwargs):
        with open('chatbot/dataset.json', 'r') as file:
            data = json.load(file)
            for item in data:
                FAQ.objects.create(question=item['question'], response=item['response'])
        self.stdout.write(self.style.SUCCESS('Successfully loaded dataset'))
