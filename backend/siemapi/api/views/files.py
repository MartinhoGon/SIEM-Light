from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from api.serializers import FileUploadSerializer
import os
from datetime import datetime
from api.utils import Parser
from api.models import Alert

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            numAlerts = 0
            file = request.FILES['file']
            current_time = datetime.now()
            formatted_time = current_time.strftime("%d-%m-%Y-%H%M%S")
            file_name = formatted_time+'_'+file.name
            
            file_path = os.path.join(settings.BASE_DIR,'file_uploads', file_name)
            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            if file_name.endswith('.log'):
                ip_dates = Parser.extractLogInfo(file_path)
                numAlerts = Alert.validateIpsFromUploadedLogs(ip_dates)
                return Response({"message": "The uploaded file returned a total of {} alerts.".format(numAlerts)})
            elif file_name.endswith('.pcap'):
                numAlerts = Parser.parseDnsPcap(file_path)
                return Response({"message": "The uploaded file returned a total of {} alerts.".format(numAlerts)})
        return Response({"message": serializer.errors['file']}, status=status.HTTP_400_BAD_REQUEST)
