from django.shortcuts import render
#from django.http import JsonResponse
#from rest_framework import generics
from api.models import Value
from api.serializers import ValueSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#Get a list of all values
# def valueList(request):
#     values = Value.objects.all()
#     serializer = ValueSerializer(values, many=True)
#     return Response(serializer.data, safe=False)


class ValueList(APIView):
    """
    List all values, or create a new snippet.
    """
    def get(self, request, format=None):
        values = Value.objects.all()
        serializer = ValueSerializer(values, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = ValueSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValueDetail(APIView):
    """
    Retrieve, update or delete a value instance.
    """
    def get_object(self, pk):
        try:
            return Value.objects.get(pk=pk)
        except Value.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        value = self.get_object(pk)
        serializer = ValueSerializer(value)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     value = self.get_object(pk)
    #     serializer = ValueSerializer(value, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     value = self.get_object(pk)
    #     value.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)