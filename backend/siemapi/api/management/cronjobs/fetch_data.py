from api.models import Feed, Value
from api.utils import DataFetcher, Parser
from datetime import datetime

def get_feed():
    #Starting by decreasing all values by 1:
    Value.decrementCheckValue()
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print("{} -  Starting fetching data from feeds".format(formatted_datetime))
    feeds = Feed.objects.all()
    for feed in feeds:
        data = DataFetcher.fetch(feed)
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print("{} -  Getting feed {}".format(formatted_datetime, feed.name))
        if data:
            if feed.parser == 'txt':
                data = Parser.parseText(data)
                Value.createValues(feed, data)
            elif feed.parser == 'csv':
                data = Parser.parseCSV(feed.delimeter, feed.delimeterField, data)
                Value.createValues(feed, data)
            elif feed.parser == 'json':
                print('parser json')
                # pass
            else:
                print("Undefined parser")
        else:
            pass
            #self.stdout.write(self.style.ERROR(f'Failed to fetch data from feed: {feed.url}'))
        # break
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print("{} -  Ending fetching data from feeds".format(formatted_datetime))


