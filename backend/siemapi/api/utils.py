import requests, pyshark
from api.models import Value, Alert
from api.logger import get_logger

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
        alertCounter = 0
        for packet in capture:
            if hasattr(packet, 'dns'):
                if packet.dns.count_answers > "0":
                    strAlert = ''
                    if Value.searchValue(packet.dns.qry_name):
                        strAlert = 'A DNS request to {} was made from {}. This domain is a match to the internal database'.format(packet.dns.qry_name,packet.ip.dst)
                        alertCounter += Alert.createAlert(packet.dns.qry_name, strAlert)
                    if Value.searchValue(packet.ip.src):
                        strAlert = "This IP Address {} returned a response to a DNS query from {}. This IP address is a match to the internal database.".format(packet.ip.src,packet.ip.dst)
                        alertCounter += Alert.createAlert(packet.dns.qry_name, strAlert)
                    if hasattr(packet.dns, "a"):
                        if Value.searchValue(packet.dns.a):
                            strAlert = "A DNS request returned a known malicious IP address ({}) from a query made by {}. This IP address is a match to the internal database.".format(packet.ip.a,packet.ip.src)
                    else:
                        if Value.searchValue(packet.dns.ptr_domain_name):
                            strAlert = 'A DNS request to {} was made from {}. This domain is a match to the internal database'.format(packet.ptr_domain_name,packet.ip.dst)
                            alertCounter += Alert.createAlert(packet.dns.qry_name, strAlert)
        logger.info('Endded DNS traffic parsing')
        return alertCounter
