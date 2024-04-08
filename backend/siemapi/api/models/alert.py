from django.db import models
from enum import Enum

class ValueType(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'

class Alert(models.Model):
    level = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in ValueType])
    message = models.TextField()
    
    def __str__(self):
        return self.name