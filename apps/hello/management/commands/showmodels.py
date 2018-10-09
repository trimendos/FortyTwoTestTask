from django.core.management.base import BaseCommand
from django.db.models import get_models


class Command(BaseCommand):
    help = 'Prints all model there is in DB and the count of their objects.'

    def handle(self, *args, **options):
        self.stdout.write('Model name - Count of objects')
        for model in get_models():
            msg = '{0} - {1}'.format(model.__name__, model.objects.count())
            self.stdout.write(msg)
            self.stderr.write('Error: {0}'.format(msg))
