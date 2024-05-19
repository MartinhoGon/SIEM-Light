from rest_framework import serializers
from api.models import *

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["id", "level", "message", "acknowledge"]



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ["id", "category", "name", "url", "parser", "refresh", 'delimeter', "delimeterField"]


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ["id", "value", "type", "checkValue"]


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(('.log', '.pcap')):
            raise serializers.ValidationError('File must be a .log or .pcap')
        return value