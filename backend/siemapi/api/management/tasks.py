from celery import shared_task
from api.models import Feed
from api.utils import DataFetcher

@shared_task
def fetch_all_feeds_data():
    feeds = Feed.objects.all()
    for feed in feeds:
        fetch_feed_data.delay(feed.id)