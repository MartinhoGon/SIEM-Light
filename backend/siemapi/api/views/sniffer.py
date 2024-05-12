from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pyshark

sniffer = None

@csrf_exempt
def start_sniffer(request):
    global sniffer
    
    if sniffer is None:
        sniffer = pyshark.LiveCapture(interface='ens33', bpf_filter='port 53')
        sniffer.apply_on_packets(packet_handler)
        return JsonResponse({"message": "Sniffer started successfully."}, status=200)
    else:
        return JsonResponse({"message": "Sniffer is already running."}, status=200)

@csrf_exempt
def stop_sniffer(request):
    global sniffer
    
    if sniffer:
        sniffer.close()
        sniffer = None
        return JsonResponse({"message": "Sniffer stopped successfully."}, status=200)
    else:
        return JsonResponse({"message": "Sniffer is not running."}, status=200)

def packet_handler(packet):
    # Implement packet handling logic here
    pass
