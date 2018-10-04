from django.core.urlresolvers import reverse
from django.test import TestCase

from apps.hello.models import Request


class RequestMiddlewareTest(TestCase):
    def setUp(self):
        Request.objects.all().delete()

    def test_process_requests_to_nonexistent_page(self):
        """Test processing the request to nonexistent page"""
        self.assertEqual(Request.objects.all().count(), 0)
        self.assertEqual(self.client.get('/some_page').status_code, 404)
        self.assertEqual(Request.objects.all().count(), 1)

    def test_process_request_to_existent_page(self):
        """Test processing the request to existent page"""
        self.assertEqual(Request.objects.all().count(), 0)
        self.assertEqual(
            self.client.get(reverse('main_page')).status_code, 200
        )
        self.assertEqual(Request.objects.all().count(), 1)

    def test_request_data_saved_correct(self):
        """Test middleware makes record with correct data"""
        self.client.get('/')
        last_request = Request.objects.last()
        self.assertEqual(last_request.method, 'GET')
        self.assertEqual(last_request.url, '/')
        self.assertEqual(last_request.status_code, 200)

    def test_quantity_of_new_requests(self):
        """Test amount of recent requests is the correct"""
        self.client.get('/')
        self.client.post('/')
        requests = Request.objects.all()
        self.assertEqual(requests.count(), 2)
        self.assertEqual(requests.filter(method='POST').count(), 1)
        self.assertEqual(requests.filter(method='GET').count(), 1)

    def test_mark_as_unviewed(self):
        """If requested page is not requests_page, mark the request as unviewed
        """
        self.client.get('/')
        self.assertEqual(Request.objects.first().viewed, False)
