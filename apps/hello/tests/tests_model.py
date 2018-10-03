# -*- coding: utf-8 -*-
from datetime import date
from factory import fuzzy, DjangoModelFactory

from django.test import TestCase
from apps.hello.models import Profile, Request


class RequestFactory(DjangoModelFactory):
    class Meta:
        model = Request
    datetime = fuzzy.FuzzyDate(date.today())


class TestProfile(TestCase):
    """Test model Profile"""
    def test_unicode_string_representation(self):
        """Test method __unicode__"""
        profile = Profile(first_name=u'Роман', last_name=u'Дузь')
        self.assertEqual(unicode(profile), u'Дузь Роман')

    def test_fields_in_model(self):
        """Test all fields are present in the model"""
        fields = {k.name: k.get_internal_type() for k in Profile._meta.fields}
        self.assertDictEqual(fields, {
                        u'id': u'AutoField',
                        'first_name': u'CharField',
                        'biography': u'TextField',
                        'last_name': u'CharField',
                        'birthday': u'DateField',
                        'contacts': u'TextField',
                        'jabber': u'CharField',
                        'email': u'CharField',
                        'skype': u'CharField',
        })


class TestRequest(TestCase):
    """Test model Request"""
    def test_unicode_string_representation(self):
        """Test method __unicode__"""
        request = Request(url='/', datetime='03/Oct/2018 13:19:45')
        self.assertEqual(unicode(request), u'03/Oct/2018 13:19:45 /')

    def test_fields_in_model(self):
        """Test all fields are represented in the model"""
        fields = {k.name: k.get_internal_type() for k in Request._meta_fields}
        self.assertDictEqual(fields, {
            u'id': u'AutoField',
            'datetime': u'DateTimeField',
            'url': u'CharField',
            'status_code': u'IntegerField',
            'method': u'CharField',
            'viewed': u'BooleanField'
        })

    def test_get_unviewed_count(self):
        """Model can return the count of unviewed objects"""
        for _ in range(7):
            RequestFactory.create(status_code=200)
        self.assertEqual(Request.get_unviewed_count(), 7)
