import requests
from api.models import Value
import logging
from django.conf import settings

def get_logger():
    logger = logging.getLogger(settings.CUSTOM_LOGGER_NAME)
    return logger

class DataFetcher:
    @staticmethod
    def fetch(feed):
        url = feed.url
        response = requests.get(url)
        if response.status_code == 200:
            return response.json() if response.headers.get('content-type') == 'application/json' else response.content
        else:
            return None

class Parser:
    @staticmethod
    def parseText(data):
        data = data.decode("utf-8")
        values = data.split('\n')
        return values

    @staticmethod
    def parseCSV(delimeter, field, data):
        data = data.decode("utf-8").split('\n')
        values = []
        for line in data:
            if not line.startswith("#"):
                values.append(line.split(delimeter)[field])
        return values

    @staticmethod
    def parseDnsPcap(file_name):
        logger = get_logger()
        logger.info('Starting to parse DNS traffic')
        capture = pyshark.FileCapture(file_name)
        for packet in capture:
            if hasattr(packet, 'dns'):
                if packet.dns.count_answers > "0":
                    # This will crossreference between all the IP addresses and domain names collected by the feeds
                    # If it gets any match it will create an alert
                    print("Query:"+ packet.dns.qry_name)
                    print("DNS Server:"+ packet.ip.src) # neste caso é o ip do dns server
                    print("Client:"+ packet.ip.dst) # quem fez o pedido
                    if hasattr(packet.dns, "a"):
                        print("Response: "+ packet.dns.a)
                    else:
                        print("Response: "+ packet.dns.ptr_domain_name)
        logger.info('Endded DNS traffic parsing')
