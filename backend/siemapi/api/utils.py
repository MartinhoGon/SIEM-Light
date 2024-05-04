import requests
from api.models import Value

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