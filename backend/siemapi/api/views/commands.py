from rest_framework.views import APIView
import os
from signal import SIGTERM
import time
import psutil
from rest_framework.response import Response
from subprocess import Popen, PIPE
# import subprocess
from api.models import Helper
from api.utils import Parser
from api.logger import get_logger
from api.serializers import PortSerializer

class StartListener(APIView):
    def post(self, request):
        logger = get_logger()
        if Helper.objects.exists():
            helper = Helper.objects.first()
        else:
            helper = Helper.objects.create()

        if request.data.get("port"):
            serializer = PortSerializer(data=request.data)
            if serializer.is_valid():
                if int(request.data.get("port")) < 1024:
                    return Response({"message": "The choosen port must be between 1024 and 65535."}, status=400)
                port = str(request.data.get("port"))
            else:
                return Response(serializer.errors, status=400)
        else:
            port = "32000"
        
        if not helper.is_listener_running:
            # Start netcat listener
            #process = Popen(['nc -l 32000 > file.pcap'], shell=True, stdout=PIPE, stderr=PIPE)
            try:
                with open('file.pcap', 'wb') as output_file:
                    command = ["nc", "-l", port]
                    process = Popen(command, stdout=output_file, stderr=PIPE)
                    pid = process.pid  # Get the PID of the subprocess
                    helper.is_listener_running = True
                    helper.listener_pid = process.pid
                    helper.save()
                    logger.info('Started the listener')
                    return Response({"message": "Listener started successfully."}, status=200)  
            except Exception as e:
                logger.error('Error while starting the listener')
                return Response({"message": "Error while starting the listener. {}".format(e)}, status=400)
        else:
            return Response({"message": "Listener is already running."})

class StopListener(APIView):
    def post(self, request):
        logger = get_logger()
        if Helper.objects.exists():
            helper = Helper.objects.first()
            if helper.is_listener_running:
                # Stop netcat listener
                os.kill(helper.listener_pid, SIGTERM)
                helper.is_listener_running = False
                helper.listener_pid = 0
                helper.save()
                numAlerts = Parser.parseDnsPcap('file.pcap')
                logger.info('Listener stopped successfuly')
                return Response({"message": "Listener stopped. The DNS capture returned a total of {} alerts.".format(numAlerts)}, status=200)
            else:
                return Response({"message": "Listener is not running."}, status=200)
        else:
            return Response({"message": "Listener is not running."}, status=200)

class StartSniffer(APIView):
    def post(self, request):
        logger = get_logger()
        if Helper.objects.exists():
            helper = Helper.objects.first()
        else:
            helper = Helper.objects.create()
        if request.data.get("interface"):
            interface = request.data.get("interface")
            interfaces = psutil.net_if_addrs()

            if interface not in interfaces:
                return Response({"message": "Invalid interface."}, status=400)
        else:
            return Response({'message': 'Interface not provided'}, status=400)
        if not helper.is_sniffer_running:
            try:
                cmd = ["python", "networkSniffer.py", interface]
                process =  Popen(cmd, stdout=PIPE, stderr=PIPE)
                helper.is_sniffer_running = True
                helper.sniffer_pid = process.pid
                helper.save()
                logger.info('Sniffer started successfuly')
                return Response({"message": "Sniffer started successfully."}, status=200)
            except Exception as e:
                logger.error('Error while starting the sniffer')
                return Response({"message": "Error while starting the sniffer. {}".format(e)}, status=400)
                # return JsonResponse({"error": str(e)}, status=500)
        else: 
            return Response({"message": "Sniffer is already running."}, status=200)


class StopSniffer(APIView):
    def post(self, request):
        logger = get_logger()
        if Helper.objects.exists():
            helper = Helper.objects.first()
            if helper.is_sniffer_running:
                os.kill(helper.sniffer_pid, SIGTERM)
                helper.is_sniffer_running = False
                helper.sniffer_pid = 0
                helper.save()
                logger.info('Sniffer stopped successfuly')
                return Response({"message": "Sniffer stopped. Check the alerts to see if any were created"}, status=200)
            else:
                return Response({"message": "Sniffer is not running."}, status=200)
        else:
            return Response({"message": "Sniffer is not running."}, status=200)