from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Prints all model there is in DB and the count of their objects.'

    def handle(self, *args, **options):
        pass
