from rest_framework.views import APIView
import os
from signal import SIGTERM
import time
from rest_framework.response import Response
from subprocess import Popen, PIPE
# import subprocess
from api.models import Helper
from api.utils import get_logger, Parser

class StartListener(APIView):
    def post(self, request):
        logger = get_logger()
        if Helper.objects.exists():
            helper = Helper.objects.first()
        else:
            helper = Helper.objects.create()
        
        if not helper.is_listener_running:
            # Start netcat listener
            #process = Popen(['nc -l 32000 > file.pcap'], shell=True, stdout=PIPE, stderr=PIPE)
            try:
                with open('file.pcap', 'wb') as output_file:
                    command = ["nc", "-l", "32000"]
                    process = Popen(command, stdout=output_file, stderr=PIPE)
                    pid = process.pid  # Get the PID of the subprocess
                    helper.is_listener_running = True
                    helper.listener_pid = process.pid
                    helper.save()
                    logger.info('Started the listener')
                    return Response({"message": "Listener started."})  
            except Exception as e:
                logger.error('Error while starting the listener successfuly')
                return Response({"message": "Error while starting the listener."})
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
                return Response({"message": "Listener stopped. The DNS capture returned a total of {} alerts.".format(numAlerts)})
            else:
                return Response({"message": "Listener is not running."})
        else:
            return Response({"message": "Listener is not running."})

# class StartSniffer(APIView):
#     def post(self, request):
#         capture = pyshark.LiveCapture(interface=interface, bpf_filter=shark_filter)
#         try:
#             for packet in capture.sniff_continuously(packet_count=100):
#                 if hasattr(packet, 'dns'):
#                     pass