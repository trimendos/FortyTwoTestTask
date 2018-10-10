# -*- coding: utf-8 -*-
from json import loads
from datetime import date, datetime
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
    fixtures = ['webrequests']

    def setUp(self):
        self.url = reverse('requests_page')
        self.response = self.client.get(self.url)

    def test_page_returned(self):
        """Test requests page is returned"""
        self.url = reverse('requests_page')
        self.response = self.client.get(self.url)
        self.assertEqual(
            self.response.status_code, 200, 'Page was not returned'
        )
        self.assertContains(self.response, 'Requests')
        self.assertTemplateUsed(self.response, 'hello/requests_page.html')

    def test_change_priority_async_valid_data(self):
        """Changing priority invoke updating record with given "id"."""
        new_priority = 10
        rq = Request.objects.last()
        response = self.client.post(
            reverse('requests_page'),
            data={
                'rq_id': rq.id,
                'priority': new_priority,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        webrequests = loads(response.content)['webrequests']
        rq_list = Request.objects.all().order_by('-priority')
        self.assertEqual(webrequests[0]['id'], rq_list.first().id)

    def test_change_priority_async_non_valid(self):
        """Should return error dict"""
        new_priority = -10
        rq = Request.objects.last()
        response = self.client.post(
            reverse('requests_page'),
            data={
                'id': rq.id,
                'priority': new_priority,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        content = loads(response.content)
        self.assertTrue(content.get('errors', False))

    def test_10_requests_sorting_by_newest_datetime_ajax_request(self):
        """View returns web requests from newest one. Request via ajax"""
        response = self.client.get(
            reverse('requests_page') + '?sort_datetime=last',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        objects = loads(response.content)['webrequests']

        self.assertEqual(len(objects), 10)
        self.assertGreater(
            datetime.strptime(objects[0]['datetime'], '%d/%b/%Y %H:%M:%S'),
            datetime.strptime(objects[-1]['datetime'], '%d/%b/%Y %H:%M:%S')
        )

    def test_10_requests_sorting_by_oldest_datetime_ajax_request(self):
        """View returns web requests from oldest one. Request via ajax"""
        response = self.client.get(
            reverse('requests_page') + '?sort_datetime=first',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        objects = loads(response.content)['webrequests']
        self.assertGreater(
            datetime.strptime(objects[-1]['datetime'], '%d/%b/%Y %H:%M:%S'),
            datetime.strptime(objects[0]['datetime'], '%d/%b/%Y %H:%M:%S')
        )

    def test_10_requests_sorting_by_decreasing_priority_ajax_request(self):
        """View returns requests with priority from highest to lowest.
        Request via ajax"""
        Request.update_priority(1, 2)

        response = self.client.get(
            reverse('requests_page') + '?sort_priority=high',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        objects = loads(response.content)['webrequests']

        self.assertGreater(objects[0]['priority'], objects[-1]['priority'])

    def test_10_last_requests_sorting_by_ascending_priority_ajax_request(self):
        """View returns requests with priority from lowest to highest.
        Request via ajax"""
        Request.update_priority(1, 2)

        response = self.client.get(
            reverse('requests_page') + '?sort_priority=low',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        objects = loads(response.content)['webrequests']

        self.assertGreater(objects[-1]['priority'], objects[0]['priority'])


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
        self.kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        self.credentials = {'username': 'admin',
                            'password': 'admin'}

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
        self.client.login(**self.credentials)
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

    def test_ajax_invalid_post(self):
        """Profile should not be updated"""
        fields = [k for k, v in ProfileUpdateForm.base_fields.iteritems()
                  if v.required]
        data = dict.fromkeys(fields, u"")
        self.client.login(**self.credentials)
        response = self.client.post(self.url, data, **self.kwargs)
        ERROR_MESSAGE = 'This field is required.'
        self.assertContains(response, ERROR_MESSAGE, 6, 400)
        profile = Profile.objects.first()
        for field in fields:
            self.assertNotEqual(profile.serializable_value(field),
                                data[field])

    def test_ajax_valid_post(self):
        """Profile should be updated"""
        self.client.login(**self.credentials)
        data = {'first_name': 'Linus',
                'last_name': 'Torvalds',
                'birthday': '28/12/1969',
                'email': 'l.torvalds@test.com',
                'skype': 'l.torvalds',
                'jabber': 'l.torvalds@test.com',
                'contacts': 'exist',
                'biography': 'Torvalds was born in Helsinki, Finland.'}
        response = self.client.post(self.url, data, **self.kwargs)
        self.assertEqual(response.status_code, 200)
        profile = Profile.objects.first()
        self.assertEqual(profile.first_name, data['first_name'])
        self.assertEqual(profile.last_name, data['last_name'])
        self.assertEqual(
            profile.birthday.strftime('%d/%m/%Y'), data['birthday'])
        self.assertEqual(profile.email, data['email'])
        self.assertEqual(profile.jabber, data['jabber'])
        self.assertEqual(profile.contacts, data['contacts'])
        self.assertEqual(profile.biography, data['biography'])
