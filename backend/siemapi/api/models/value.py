from django.db import models
from enum import Enum

class ValueType(Enum):
    DOMAIN = 'Domain'
    IP_ADDRESS = 'IP Address'

class Value(models.Model):
    type = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in ValueType])
    description = models.CharField(max_length=250, null=True)
    value = models.CharField(max_length=500)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField()

    def __str__(self):
        return f"{self.type} - {self.value}"