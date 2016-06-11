from django.core.management.base import BaseCommand
from kettle.scripts.trainClassifier import test_run

class Command(BaseCommand):
    help = 'Refreshes the Beer models'

    def handle(self, *args, **options):
        test_run()


