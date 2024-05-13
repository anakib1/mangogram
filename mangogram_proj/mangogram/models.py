# messages/models.py
from django.db import models

class Message(models.Model):
    timestamp = models.IntegerField()
    content = models.JSONField()
    userId = models.CharField(max_length=100)  # Assuming userId is a string field
