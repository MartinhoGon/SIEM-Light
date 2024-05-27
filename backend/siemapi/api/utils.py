import requests, pyshark
from api.models import Value, Alert
from api.logger import get_logger
import re

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
            alertCounter = Parser.handle_packet(packet, alertCounter)
        logger.info('Endded DNS traffic parsing')
        return alertCounter

    def handle_packet(packet, alertCounter):
        logger = get_logger()
        if hasattr(packet, 'dns') and hasattr(packet, 'ip'):
            if packet.dns.count_answers > "0":
                strAlert = ''
                # logger.info("Checking "+ packet.dns.qry_name)
                if Value.searchValue(packet.dns.qry_name):
                    strAlert = 'A DNS request to {} was made from {}. This domain is a match to the internal database'.format(packet.dns.qry_name,packet.ip.dst)
                    alertCounter = alertCounter + Alert.createAlert(packet.dns.qry_name, strAlert)
                if Value.searchValue(packet.ip.src):
                    strAlert = "This IP Address {} returned a response to a DNS query from {}. This IP address is a match to the internal database.".format(packet.ip.src,packet.ip.dst)
                    alertCounter = alertCounter + Alert.createAlert(packet.dns.qry_name, strAlert)
                if hasattr(packet.dns, "a"):
                    if Value.searchValue(packet.dns.a):
                        strAlert = "A DNS request returned a known malicious IP address ({}) from a query made by {}. This IP address is a match to the internal database.".format(packet.ip.a,packet.ip.src)
                        alertCounter = alertCounter + Alert.createAlert(packet.dns.a, strAlert)
                else:
                    if hasattr(packet.dns,'ptr_domain_name'):
                        if Value.searchValue(packet.dns.ptr_domain_name):
                            strAlert = 'A DNS request to {} was made from {}. This domain is a match to the internal database'.format(packet.ptr_domain_name,packet.ip.dst)
                            alertCounter = alertCounter + Alert.createAlert(packet.dns.qry_name, strAlert)
                    else:
                        pass
                        # print(packet.dns)
        elif hasattr(packet, 'dns') and hasattr(packet, 'ipv6'):
            if packet.dns.count_answers > "0":
                strAlert = ''
                # logger.info("Checking "+ packet.dns.qry_name)
                if Value.searchValue(packet.dns.qry_name):
                    strAlert = 'A DNS request to {} was made from {}. This domain is a match to the internal database'.format(packet.dns.qry_name,packet.ipv6.dst)
                    alertCounter = alertCounter + Alert.createAlert(packet.dns.qry_name, strAlert)
                if Value.searchValue(packet.ipv6.src):
                    strAlert = "This IP Address {} returned a response to a DNS query from {}. This IP address is a match to the internal database.".format(packet.ipv6.src,packet.ipv6.dst)
                    alertCounter = alertCounter + Alert.createAlert(packet.dns.qry_name, strAlert)
                if hasattr(packet.dns, "a"):
                    if Value.searchValue(packet.dns.a):
                        strAlert = "A DNS request returned a known malicious IP address ({}) from a query made by {}. This IP address is a match to the internal database.".format(packet.ipv6.a,packet.ipv6.src)
                        alertCounter = alertCounter + Alert.createAlert(packet.dns.a, strAlert)
                else:
                    if hasattr(packet.dns,'ptr_domain_name'):
                        if Value.searchValue(packet.dns.ptr_domain_name):
                            strAlert = 'A DNS request to {} was made from {}. This domain is a match to the internal database'.format(packet.ptr_domain_name,packet.ipv6.dst)
                            alertCounter = alertCounter + Alert.createAlert(packet.dns.qry_name, strAlert)
                    else:
                        pass
                        # print(packet.dns)
        return alertCounter



    @staticmethod
    def extractLogInfo(file_path):
        """
        Parses the log file and gets all IP address and corresponding datetime
        :param log_path:
        :return: Array with IP address and datetime
        """
        ip_datetime_pairs = []

        ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        datetime_pattern = r"^\w{3}\s+\d{1,2} \d{2}:\d{2}:\d{2}"

        with open(file_path, 'r') as file:
            for line in file:
                ip_matches = re.findall(ip_pattern, line)
                # print(ip_matches)
                datetime_match = re.match(datetime_pattern, line)
                if ip_matches:

                    for ip in ip_matches:
                        # print(ip)
                        datetime = '--'
                        if datetime_match:
                            if datetime_match.group(0):
                                datetime = datetime_match.group(0)
                        ip_datetime_pairs.append((ip, datetime))
        return ip_datetime_pairs
