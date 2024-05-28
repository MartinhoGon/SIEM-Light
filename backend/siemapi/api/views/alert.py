from django.shortcuts import render
#from django.http import JsonResponse
#from rest_framework import generics
from api.models import Alert
from api.serializers import AlertSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AlertList(APIView):
    """
    List all alerts, or create a new snippet.
    """
    def get(self, request, format=None):
        alerts = Alert.objects.all()
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = AlertSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlertDetail(APIView):
    """
    Retrieve, update or delete a alert instance.
    """
    def get_object(self, pk):
        try:
            return Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        alert = self.get_object(pk)
        serializer = AlertSerializer(alert)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        alert = self.get_object(pk)
        alert.acknowledge = True
        alert.save()
        serializer = AlertSerializer(alert)
        return Response(serializer.data)
    # def put(self, request, pk, format=None):
    #     alert = self.get_object(pk)
    #     serializer = AlertSerializer(alert, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     alert = self.get_object(pk)
    #     alert.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)