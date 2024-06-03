## Operating System Interface
from rest_framework.views import APIView
from signal import SIGTERM
from rest_framework.response import Response
from rest_framework import status
from api.logger import get_logger
import psutil

class OsInterface(APIView):
    """
    Retrieve, update or delete a alert instance.
    """

    def get(self, request):
        try:
            interfaces = psutil.net_if_addrs()
            interface_names = list(interfaces.keys())
            return Response({"interfaces": interface_names}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
