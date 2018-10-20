from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import profiles from Intranet API'

    def handle(self, *args, **kwargs):
        pass
