from rest_framework.views import APIView
import os
from signal import SIGTERM
import time
from rest_framework.response import Response
from subprocess import Popen, PIPE
# import subprocess
from api.models import Helper

class StartListener(APIView):
    def post(self, request):
        if Helper.objects.exists():
            helper = Helper.objects.first()
        else:
            helper = Helper.objects.create()
        
        if not helper.is_listener_running:
            # Start netcat listener
            #process = Popen(['nc -l 32000 > file.pcap'], shell=True, stdout=PIPE, stderr=PIPE)
            try:
                with open('/home/martinho/file.pcap', 'wb') as output_file:
                    command = ["nc", "-l", "32000"]
                    process = Popen(command, stdout=output_file, stderr=PIPE)
                    pid = process.pid  # Get the PID of the subprocess
                    helper.is_listener_running = True
                    helper.listener_pid = process.pid
                    helper.save()
                    return Response({"message": "Listener started."})  
            except Exception as e:
                return Response({"message": "Error while starting the listener."})
        else:
            return Response({"message": "Listener is already running."})

class StopListener(APIView):
    def post(self, request):
        if Helper.objects.exists():
            helper = Helper.objects.first()
            if helper.is_listener_running:
                # Stop netcat listener
                os.kill(helper.listener_pid, SIGTERM)
                helper.is_listener_running = False
                helper.listener_pid = 0
                helper.save()
                return Response({"message": "Listener stopped."})
            else:
                return Response({"message": "Listener is not running."})
        else:
            return Response({"message": "Listener is not running."})