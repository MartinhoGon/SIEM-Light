from django.shortcuts import render
from django.http import JsonResponse
#from rest_framework import generics
from api.models.feed import Feed
from api.serializers.feed import FeedSerializer

#Get a list of all feeds
def feedList(request):
    feeds = Feed.objects.all()
    serializer = FeedSerializer(feeds, many=True)
    return JsonResponse(serializer.data, safe=False)
