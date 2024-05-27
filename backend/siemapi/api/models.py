from django.db import models
from enum import Enum
import re
from api.logger import get_logger
from datetime import datetime

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

    @staticmethod
    def checkAlertLevel(checkValue):
        numFeeds = Feed.objects.count()
        preLevel = checkValue/numFeeds
        if preLevel == 1:
            return 'Critical'
        elif 0.9 <= preLevel <= 1:
            return 'High'
        elif 0.4 <= preLevel < 0.9:
            return 'Medium'
        elif 0.24 <= preLevel < 0.4:
            return 'Low'
    
    @staticmethod
    def createAlert(queryValue, message):
        logger = get_logger()
        try:
            value = Value.objects.filter(value=queryValue).first()
            # if value is not None:
                # logger.info('Value Exists {}'.format(value.value))
            alertLevel = Alert.checkAlertLevel(value.checkValue)
            current_time = datetime.now()
            formatted_time = current_time.strftime("%d-%m-%Y-%H%M%S")
            newMessage = alertLevel+' - '+formatted_time+' - '+message
            alert = Alert(level=alertLevel, message=newMessage, acknowledge=False)
            alert.save()
            logger.info('A new alert was created.')
            return 1
        except Exception as e:
            logger.error('There was an error creating a new alert. {}'.format(e))
            return 0

    @staticmethod
    def validateIpsFromUploadedLogs(ip_dates):
        logger = get_logger()
        numAlerts = 0
        try:
            logger.info("Validating IPs from uploaded log file.")
            for pair in ip_dates:
                # ip = pair[0]
                value = Value.objects.filter(value=pair[0]).first()
                if value:
                    message = 'The IP address {} was detected in the uploaded log file. This IP address is a match to the internal database'.format(pair[0])
                    numAlerts = numAlerts + Alert.createAlert(pair[0], message)

            return numAlerts
        except Exception as e:
            logger.error('There was an error validating {}'.format(e))
            return 0
        
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

    @staticmethod
    def searchValue(queryValue):
        results = Value.objects.filter(value=queryValue)
        if results.exists():
            return True
        else:
            return False
#########
# Helper  #
#########

class Helper(models.Model):
    is_listener_running = models.BooleanField(default=False)
    listener_pid = models.IntegerField(null=True, blank=True)
    is_sniffer_running = models.BooleanField(default=False)
    sniffer_pid = models.IntegerField(null=True, blank=True)
    is_using_rsync = models.BooleanField(default=False)

