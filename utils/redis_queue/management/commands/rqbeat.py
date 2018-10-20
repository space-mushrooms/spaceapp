from django.core.management.base import BaseCommand
from django_rq import get_scheduler

from utils.redis_queue import register_cron


class Command(BaseCommand):
    """
    Runs RQ scheduler
    """
    help = __doc__
    args = '<queue>'

    def add_arguments(self, parser):
        parser.add_argument('--interval', '-i', type=int, dest='interval',
                            default=5, help="""How often the scheduler checks for new jobs to add to the
                            queue (in seconds).""")

    def handle(self, *args, **options):
        scheduler = get_scheduler(interval=options.get('interval'))

        # cancel existing jobs
        for job in scheduler.get_jobs():
            scheduler.cancel(job)
            job.delete()

        # register new jobs
        register_cron(scheduler)

        scheduler.run()
