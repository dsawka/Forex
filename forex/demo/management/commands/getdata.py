from django.core.management.base import BaseCommand, CommandError
from ._private import get_data


class Command(BaseCommand):
    help = 'Getting currency data in real time'

    def handle(self, *args, **options):
        get_data()
