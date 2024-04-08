from django.shortcuts import render
#from django.http import JsonResponse
#from rest_framework import generics
from api.models.category import Category
from api.serializers.category import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#Get a list of all categorys
# def categoryList(request):
#     categorys = Category.objects.all()
#     serializer = CategorySerializer(categorys, many=True)
#     return Response(serializer.data, safe=False)


class CategoryList(APIView):
    """
    List all categorys, or create a new snippet.
    """
    def get(self, request, format=None):
        categorys = Category.objects.all()
        serializer = CategorySerializer(categorys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    """
    Retrieve, update or delete a category instance.
    """
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)