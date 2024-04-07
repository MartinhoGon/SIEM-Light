from django.db import models
from .category import Category

class Feed(models.Model):
    JSON = 'json'
    FILE = 'file'
    CSV = 'csv'
    TYPE_CHOICES = [
        (JSON, 'JSON'),
        (FILE, 'File'),
        (CSV, 'CSV'),
    ]

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    refresh = models.DurationField()

    def __str__(self):
        return f"{self.name} - {self.category.name}"