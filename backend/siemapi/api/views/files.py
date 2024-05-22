from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from api.serializers import FileUploadSerializer
import os
from datetime import datetime
from api.utils import Parser
from api.models import Alert
from api.logger import get_logger

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        logger = get_logger()
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
                current_time = datetime.now()
                formatted_time = current_time.strftime("%d-%m-%Y-%H:%M:%S")
                logger.info("{} - Started parsing the uploaded log file.".format(formatted_time))

                ip_dates = Parser.extractLogInfo(file_path)
                numAlerts = Alert.validateIpsFromUploadedLogs(ip_dates)
                
                current_time = datetime.now()
                formatted_time = current_time.strftime("%d-%m-%Y-%H:%M:%S")
                logger.info("{} - Ended parsing the uploaded log file.".format(formatted_time))
                if os.path.exists(file_path):
                    os.remove(file_path)
                return Response({"message": "The uploaded file returned a total of {} alerts.".format(numAlerts)}, status=200)
            elif file_name.endswith('.pcap'):
                current_time = datetime.now()
                formatted_time = current_time.strftime("%d-%m-%Y-%H:%M:%S")
                logger.info("{} - Started parsing the uploaded pcap file.".format(formatted_time))
                
                numAlerts = Parser.parseDnsPcap(file_path)
                
                current_time = datetime.now()
                formatted_time = current_time.strftime("%d-%m-%Y-%H:%M:%S")
                logger.info("{} - Ended parsing the uploaded pcap file.".format(formatted_time))
                if os.path.exists(file_path):
                    os.remove(file_path)
                return Response({"message": "The uploaded file returned a total of {} alerts.".format(numAlerts)}, status=200)
        return Response({"message": serializer.errors['file']}, status=status.HTTP_400_BAD_REQUEST)
