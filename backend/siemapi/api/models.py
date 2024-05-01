from django.db import models
from enum import Enum

#########
# Alert #
#########

class AlertLevel(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'

class Alert(models.Model):
    level = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in AlertLevel])
    message = models.TextField()
    acknowledge = models.BooleanField(default=False)

    def __str__(self):
        return self.message

############
# Category #
############

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name

#########
# Feed  #
#########

class Feed(models.Model):
    JSON = 'json'
    TXT = 'txt'
    CSV = 'csv'
    TYPE_CHOICES = [
        (JSON, 'JSON'),
        (TXT, 'TXT'),
        (CSV, 'CSV'),
    ]

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    parser = models.CharField(max_length=10, choices=TYPE_CHOICES)
    refresh = models.DurationField()

    def __str__(self):
        return f"{self.name} - {self.category.name}"


from django.db import models
from enum import Enum

#########
# Value #
#########

class ValueType(Enum):
    DOMAIN = 'Domain'
    IP_ADDRESS = 'IP Address'
    PORT = "Port"

class Value(models.Model):
    type = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in ValueType])
    description = models.CharField(max_length=250, null=True)
    value = models.CharField(max_length=500)
    checkValue = models.IntegerField()
    def __str__(self):
        return f"{self.type} - {self.value}"