from api.models import Feed
from api.utils import DataFetcher, Parser

def get_feed():
    print("Getting Feeds")
    feeds = Feed.objects.all()
    for feed in feeds:
        data = DataFetcher.fetch(feed)
        print("get_feed data")
        # print(data)
        if data:
            print("data Exists")
            if feed.parser == 'txt':
                print("parse txt")
                data = Parser.parseText(data)
                print(data)
            elif feed.parser == 'csv':
                print("parser csv")
                data = Parser.parseCSV(feed.delimeter, feed.delimeterField, data)
                print(data)
            elif feed.parser == 'json':
                print('parser json')
                # pass
            else:
                print("Undefined parser")
        else:
            pass
            #self.stdout.write(self.style.ERROR(f'Failed to fetch data from feed: {feed.url}'))
        # break


