from rest_framework import serializers
from api.models.feed import Feed

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ["id", "category", "name", "url", "parser", "refresh"]