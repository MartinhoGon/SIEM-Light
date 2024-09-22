from api.models import Feed, Value
from django.db import models
from api.utils import DataFetcher, Parser
from datetime import datetime
from api.logger import get_logger

def get_feed():
    logger = get_logger()
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("{} -  Starting fetching data from feeds".format(formatted_datetime))
    logger.info("Start Get_Feed - decrementing checkValues")
    #Starting by decreasing all values by 1:
    # Value.decrementCheckValue()
    Value.objects.all().update(checkValue=models.F('checkValue') - 1)
    feeds = Feed.objects.all()
    counterData = 0
    for feed in feeds:
        data = DataFetcher.fetch(feed)
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        logger.info("{} -  Getting feed {}".format(formatted_datetime, feed.name))
        if data:
            if feed.parser == 'txt':
                data = Parser.parseText(data)
                counterData = counterData + len(data)
                Value.createValues(feed, data)
            elif feed.parser == 'csv':
                data = Parser.parseCSV(feed.delimeter, feed.delimeterField, data)
                counterData = counterData + len(data)
                Value.createValues(feed, data)
            elif feed.parser == 'json':
                print('parser json')
                # pass
            else:
                print("Undefined parser")
        else:
            pass
        # break
    deleted_count, _ = Value.objects.filter(checkValue=0).delete()
    logger.info("{} were processed in this execution of the fetch feed data method.".format(counterData))
    logger.info("Deleted {} values that had the checkValue equal to zero. This values were not found in any of the collected feeds.".format(deleted_count))
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("{} -  Ending fetching data from feeds".format(formatted_datetime))


