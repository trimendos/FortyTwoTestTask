from django.contrib.auth.models import User
from django.test import TestCase

from ..models import CRUDLog


class CRUDLoggerTest(TestCase):
    def setUp(self):
        self.obj = User.objects.create_user(username='test1', password='test1')

    def test_created_signal_logging(self):
        """Save signal logging"""
        log = CRUDLog.objects.filter(action='created', model='User')
        self.assertEqual(log.count(), 1)

    def test_deleted_signal_logging(self):
        """Test there is entry about object deleted"""
        self.obj.delete()
        log = CRUDLog.objects.filter(action='deleted', model='User')
        self.assertEqual(log.count(), 1)

    def test_updated_signal_logging(self):
        """Test there is entry in db about object updated"""
        self.obj.username = 'new_author'
        self.obj.save()
        log = CRUDLog.objects.filter(action='updated', model='User')
        self.assertEqual(log.count(), 1)
