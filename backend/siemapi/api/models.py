from django.db import models
from enum import Enum
import re

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
    delimeter = models.CharField(max_length=1, null=True, default=None, blank=True)
    delimeterField = models.IntegerField(default=0, null=True)
    def __str__(self):
        return f"{self.name} - {self.category.name}"

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
    value = models.CharField(max_length=500, unique = True)
    checkValue = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.type} - {self.value}"

    @staticmethod
    def decrementCheckValue():
        # rever este codigo fazer Query direta
        values = Value.objects.all()
        for value in values:
            value.checkValue -= 1
            value.save()

    @staticmethod
    def checkType(value):     
        ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4}|:)$'
        domain_pattern = r'\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b'
        port_pattern = r'\b\d{1,5}\b'

        # Check if the value matches any pattern
        if re.fullmatch(ipv4_pattern, value):
            return "IP Address"
        elif re.fullmatch(ipv6_pattern, value):
            return "IP Address"
        elif re.fullmatch(domain_pattern, value):
            return "Domain"
        elif re.fullmatch(port_pattern, value):
            return "Port"
        else:
            return "Domain"

    @staticmethod
    def createValues(feed, values):
        """
        First checks if value already exists.
        If it does not exist, creates the entry and then as checkValue puts half of the number of feeds (numFeeds/2)
        If it does exist, adds to the checkValue +1
        :param log_path:
        :return: Array with IP address and datetime
        """
        numFeeds = Feed.objects.count()
        for value in values:
            try:
                dbValue = Value.objects.get(value=value) 
                # Exists; Adds to checkValue +1 and saves
                dbValue.checkValue = dbValue.checkValue + 1
                dbValue.save()
            except Value.DoesNotExist:
                # Does not exist. Create a new entry
                try:
                    newValue = Value(value=value.strip(), description=feed.category.name,type=Value.checkType(value), checkValue=int(numFeeds/2))
                    newValue.save()
                except Exception as error:
                    print("Error: ", error)

#########
# Helper  #
#########

class Helper(models.Model):
    is_listener_running = models.BooleanField(default=False)
    listener_pid = models.IntegerField(null=True, blank=True)

