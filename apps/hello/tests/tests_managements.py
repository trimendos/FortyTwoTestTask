from django.core.management import call_command
from django.db.models import get_models
from django.utils.six import StringIO
from django.test import TestCase


class ShowModelsTest(TestCase):

    def setUp(self):
        self.out = StringIO()
        self.models = get_models()

    def test_returning_stderr(self):
        """Output in format: Error: <model_name> - <objects>.count()"""
        call_command('showmodels', stderr=self.out)
        for model in self.models:
            message = 'Error: {} - {}'.format(model.__name__,
                                              model.objects.count())
            self.assertIn(
                message,
                self.out.getvalue())

    def test_returning_stdout(self):
        """Output in format: <model_name> - <objects>.count()"""
        call_command('showmodels', stdout=self.out)
        for model in self.models:
            message = '{} - {}'.format(model.__name__, model.objects.count())
            self.assertIn(message, self.out.getvalue())
