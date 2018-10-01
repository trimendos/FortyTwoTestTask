# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.hello.models import Profile


class TestProfile(TestCase):
    """Test model Profile"""
    def test_unicode_string_represantation(self):
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
