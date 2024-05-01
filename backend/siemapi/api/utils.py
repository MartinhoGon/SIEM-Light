import requests

class DataFetcher:
    @staticmethod
    def fetch(feed):
        url = feed.url
        response = requests.get(url)
        if response.status_code == 200:
            return response.json() if response.headers.get('content-type') == 'application/json' else response.content
        else:
            return None