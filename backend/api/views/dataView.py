from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models/data import Data

@api_view(['GET'])
def getDataList(request):