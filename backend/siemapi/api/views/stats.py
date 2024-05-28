from rest_framework.views import APIView
from signal import SIGTERM
from rest_framework.response import Response
from api.logger import get_logger
from api.models import Feed, Alert
from api.serializers import AlertSerializer

class GetStats(APIView):
    def get(self, request):
        logger = get_logger()
        logger.info('Geting statistics')
        try:
            numFeeds = Feed.objects.count()
            numAlerts = Alert.objects.count()
            numUnseenAlerts = Alert.objects.filter(acknowledge=False).count()
            lastAlerts = Alert.objects.filter(acknowledge=False).order_by('-created_at')[:6]
            serialized_alerts = AlertSerializer(lastAlerts, many=True).data
            return Response({"numFeeds": numFeeds, "numAlerts": numAlerts, "numUnseenAlerts": numUnseenAlerts, "lastAlerts": serialized_alerts})
        except Exception as e:
                logger.error('Error while getting statistics {}'. format(e))
                return Response({"message": "Error while getting statistics"}, status=400)

        