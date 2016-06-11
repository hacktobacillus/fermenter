from django.core.management.base import BaseCommand
from kettle.utils import get_beers


class Command(BaseCommand):
    help = 'Refreshes the Beer models'

    def handle(self, *args, **options):
        get_beers(refresh_cache=True)


