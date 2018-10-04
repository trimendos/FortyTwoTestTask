# -*- coding: utf-8 -*-
from json import loads
from datetime import date
from factory import fuzzy, DjangoModelFactory

from django.test import TestCase
from django.core.urlresolvers import reverse
from apps.hello.models import Profile, Request


class ProfileFactory(DjangoModelFactory):
    birthday = fuzzy.FuzzyDate(date(1930, 1, 1))

    class Meta:
        model = Profile


class RequestFactory(DjangoModelFactory):
    datetime = fuzzy.FuzzyDate(date.today())

    class Meta:
        model = Request


class MainPageViewTest(TestCase):
    def setUp(self):
        self.url = reverse('main_page')
        self.response = self.client.get(self.url)

    def test_page_returned(self):
        """Test main page is returned"""
        profile = Profile.objects.first()
        self.assertEqual(self.response.status_code, 200,
                         'Page was not returned')
        self.assertContains(self.response, 'Profile')
        self.assertTemplateUsed(self.response, 'hello/main_page.html')
        self.assertEqual(self.response.context['profile'], profile)

    def test_more_then_one_record_in_db(self):
        """Test contact view, should return first entry from the DB"""
        ProfileFactory.create(first_name='Linus',
                              last_name='Torvalds')
        self.assertTrue(Profile.objects.count(), 2)
        contacts = Profile.objects.all()
        response = self.client.get(self.url)
        self.assertEqual(contacts[0], response.context['profile'])

    def test_cyrillic_symbols(self):
        """Check cyrillic symbol in db"""
        Profile.objects.all().delete()
        self.assertEqual(Profile.objects.count(), 0)
        ProfileFactory.create(first_name='Линус',
                              last_name='Торвальдс')
        self.assertEqual(Profile.objects.count(), 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'Линус')

    def test_all_fields_is_present_on_page(self):
        """All fields are renders"""
        contact = Profile.objects.first()
        fields = (
            'first_name', 'last_name', 'email',
            'jabber', 'skype', 'contacts')
        for field in fields:
            self.assertContains(self.response, getattr(contact, field))
        self.assertContains(self.response, 'July 7, 1990')
        bio = contact.biography.split('\r\n')
        for row in bio:
            self.assertContains(self.response, row.replace("'", '&#39;'))

    def test_no_data_in_db(self):
        """Test when there is no data in db"""
        Profile.objects.all().delete()
        contacts = Profile.objects.first()
        self.assertEqual(Profile.objects.count(), 0)
        response = self.client.get(self.url)
        self.assertEqual(contacts, None)
        self.assertContains(response, 'The biography in db is not found.')


class RequestsPageViewTest(TestCase):
    def setUp(self):
        self.url = reverse('requests_page')
        self.response = self.client.get(self.url)

    def test_page_returned(self):
        """Test requests page is returned"""
        self.assertEqual(
            self.response.status_code, 200, 'Page was not returned'
        )
        self.assertContains(self.response, 'Requests')
        self.assertTemplateUsed(self.response, 'hello/requests_page.html')

    def test_view_returns_last_10_web_requests_by_ajax(self):
        """Returns last 10 requests on ajax request"""
        Request.objects.all().delete()
        for _ in range(10):
            RequestFactory.create(status_code=200)
        response = self.client.get(
            reverse('requests_page'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        requests = loads(response.content)['webrequests']
        # Last request
        self.assertEqual(requests[0]['id'], 10)

        # Oldest request
        self.assertEqual(requests[9]['id'], 1)

    def test_mark_all_requests_as_viewed(self):
        """If requested is requests_page and request is ajax and page is in
        focus, mark all requests in the db as viewed"""
        self.client.get('/')
        self.client.get('/some_page')
        self.client.get(
            '/requests_page/?infocus=true',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(all(r.viewed for r in Request.objects.all()))

    def test_non_mark_requests(self):
        """If requested is requests_page and request is ajax and page is not in
        focus, non mark all requests in the db as viewed"""
        self.client.get('/')
        self.client.get('/some_page')
        self.client.get(
            '/requests_page/?infocus=false',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertFalse(all(r.viewed for r in Request.objects.all()))
