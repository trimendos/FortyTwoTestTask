# -*- coding: utf-8 -*-
from json import loads
from datetime import date
from factory import fuzzy, DjangoModelFactory

from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, AnonymousUser

from apps.hello.models import Profile, Request
from ..forms import ProfileUpdateForm
from ..views import ProfileUpdatePageView


class ProfileFactory(DjangoModelFactory):
    birthday = fuzzy.FuzzyDate(date(1930, 1, 1))

    class Meta:
        model = Profile


class RequestModelFactory(DjangoModelFactory):
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
            RequestModelFactory.create(status_code=200)
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


class TestProfileUpdateView(TestCase):

    def setUp(self):
        self.pk = 1
        self.rf = RequestFactory()
        self.url = reverse('update_profile_page', kwargs={'pk': self.pk})
        self.request = self.rf.get(self.url)
        self.user = User.objects.first()
        self.request.user = self.user
        self.response = ProfileUpdatePageView.as_view()(
            self.request, pk=self.pk)

    def test_get_update_page_with_authorization(self):
        """Test should return template update_profile_page.html"""
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.template_name,
                         ['hello/update_profile_page.html'])

    def test_get_update_page_with_anonymous(self):
        """Test view should redirect on the login page"""
        request = self.rf.get(self.url)
        request.user = AnonymousUser()
        response = ProfileUpdatePageView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,
                         '/accounts/login/?next=/update_profile_page/1/')

    def test_view_return_form_with_image_field(self):
        """Field 'photo' should be in the form"""
        self.assertIsInstance(
            self.response.context_data['form'], ProfileUpdateForm)
        self.assertIn('photo', self.response.context_data['form'].fields)

    def test_get_update_page_without_pk(self):
        """Request "update_profile_page" without arg 'pk'. Return 404."""
        response = self.client.get('/update_profile_page/')
        self.assertEqual(response.status_code, 404)

    def test_get_update_page_with_wrong_pk(self):
        """Request "update_profile_page" with pk=0. Return 404."""
        self.client.login(**{'username': 'admin',
                             'password': 'admin'})
        response = self.client.get('/update_profile_page/0/')
        self.assertEqual(response.status_code, 404)

    def test_fields_presented(self):
        """Test all fields are presented on the page"""
        fields = [i.name for i in Profile._meta.fields if i.name != 'id']
        error_message = 'field "{}" is not found on the page'
        for field in fields:
            self.assertIn(
                'id="id_{0}"'.format(field),
                self.response.rendered_content, error_message.format(field))
