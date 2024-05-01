from rest_framework import serializers
from api.models.value import Value

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ["id", "value", "type", "first_seen", "last_seen"]