from django.db import models

class Data(models.Model):
    dataType = models.CharField(max_length=100)
    value = models.CharField(unique=True)
    # add more fields as needed