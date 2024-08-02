from django.shortcuts import render
#from django.http import JsonResponse
#from rest_framework import generics
from api.models import Feed
from api.serializers import FeedSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#Get a list of all feeds
# def feedList(request):
#     feeds = Feed.objects.all()
#     serializer = FeedSerializer(feeds, many=True)
#     return Response(serializer.data, safe=False)


class FeedList(APIView):
    """
    List all feeds, or create a new regestry.
    """
    def get(self, request, format=None):
        feeds = Feed.objects.all()
        serializer = FeedSerializer(feeds, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedDetail(APIView):
    """
    Retrieve, update or delete a feed instance.
    """
    def get_object(self, pk):
        try:
            return Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        feed = self.get_object(pk)
        serializer = FeedSerializer(feed)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        feed = self.get_object(pk)
        serializer = FeedSerializer(feed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        feed = self.get_object(pk)
        feed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)