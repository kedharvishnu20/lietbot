from django.db import models

class FAQ(models.Model):
    question = models.TextField()
    response = models.TextField()

class UnansweredQuestion(models.Model):
    question = models.TextField()
    response = models.TextField(blank=True, null=True)
