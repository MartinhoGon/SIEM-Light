from rest_framework.views import APIView
from signal import SIGTERM
from rest_framework.response import Response
from rest_framework import status
from api.logger import get_logger
from api.serializers import HelperSerializer
from api.models import Helper

class HelperDetail(APIView):
    """
    Retrieve, update or delete a alert instance.
    """
    def get_object(self, pk):
        try:
            return Helper.objects.get(pk=pk)
        except Helper.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        alert = self.get_object(pk)
        serializer = HelperSerializer(alert)
        return Response(serializer.data)
    
    def put(self, request, pk):
        feed = self.get_object(pk)
        serializer = HelperSerializer(feed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
