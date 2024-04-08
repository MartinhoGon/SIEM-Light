from rest_framework import serializers
from api.models.alert import Alert

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["id", "level", "message"]