from django.db import models
from enum import Enum

class AlertLevel(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'

class Alert(models.Model):
    level = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in AlertLevel])
    message = models.TextField()

    def __str__(self):
        return self.name