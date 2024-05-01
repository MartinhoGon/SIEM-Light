from django_cron import CronJobBase, Schedule
from api.models.feed import Feed
from api.utils import DataFetcher

class FetchDataCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Run every hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.fetch_data_cron_job'  # A unique code for the cron job

    def do(self):
        feeds = Feed.objects.all()
        for feed in feeds:
            data = DataFetcher.fetch(feed)
            if data:
                # Process the fetched data as needed
                # For example, save it to the database
                pass
            else:
                self.stdout.write(self.style.ERROR(f'Failed to fetch data from {feed.url}'))
