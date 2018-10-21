from django.core.management.base import BaseCommand

from app.tools.update_agency import update_agency
from app.tools.update_launch import update_launch
from app.tools.update_rocket import update_rocket


class Command(BaseCommand):
    help = 'Import data'

    def handle(self, *args, **kwargs):

        update_agency()
        update_rocket()
        update_launch()
