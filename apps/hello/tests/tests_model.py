# -*- coding: utf-8 -*-
from os import remove, path
from random import randint
from datetime import date

from factory import fuzzy, DjangoModelFactory
from PIL import Image

from django.core.files import File
from django.test import TestCase
from django.conf import settings

from apps.hello.models import Profile, Request


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile
    birthday = fuzzy.FuzzyDate(date(1940, 1, 1))


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
                        'photo': u'ImageField'
        })


class TestProfilePhotoField(TestCase):
    """TestClass for testing profile field "photo" """

    def calculate_new_size(self, input_size):
        """Calculate the dimensions of the resized image
        Args:
            input_size (tuple): Width and height of resized image.
        """
        size = (200, 200)
        x, y = input_size

        if x > size[0]:
            y = int(max(y * size[0] / x, 1))
            x = int(size[0])
        if y > size[1]:
            x = int(max(x * size[1] / y, 1))
            y = int(size[1])
        size = x, y
        return size

    def create_profile_with_photo(self):
        min_rand_int = 1
        max_rand_int = 2000
        tmp_image_size = (randint(min_rand_int, max_rand_int),
                          randint(min_rand_int, max_rand_int))
        self.input_image_size = tmp_image_size
        self.img_tmp_patn = "".join([settings.STATICFILES_DIRS[0],
                                     '/img/test_img_1.png'])

        image = Image.new('L', size=self.input_image_size)
        image.save(self.img_tmp_patn, 'PNG')
        self.expect_size = self.calculate_new_size(image.size)
        with open(self.img_tmp_patn) as f:
            profile = ProfileFactory.create(photo=File(f))
        return profile

    def setUp(self):
        Profile.objects.all().delete()
        self.profile = self.create_profile_with_photo()
        self.photo = self.profile.photo

    def tearDown(self):
        remove(self.photo.path)
        remove(self.img_tmp_patn)

    def test_image_resizing_process_if_photo_existing_in_profile(self):
        """If there is a photo in profile, resizing process should't run"""
        person = Profile.objects.last()
        photo_changed_time = path.getmtime(person.photo.path)
        person.save()
        self.assertEqual(photo_changed_time, path.getmtime(person.photo.path),
                         'Resizing the image has been performed.')

    def test_image_resizing_process_for_new_profile(self):
        """Process of resizing photos must be started only for new profile"""
        profile_photo_size = Image.open(self.profile.photo.path).size
        message = 'Photo should be scaled to 200x200, maintaining ' \
                  'aspect ratio, before saving. ' \
                  'Input: {0}, Expected: {1}, Returned: {2}'
        self.assertTupleEqual(
            self.expect_size,
            profile_photo_size,
            message.format(
                self.input_image_size, self.expect_size, profile_photo_size))


class TestRequest(TestCase):
    """Test model Request"""
    def test_unicode_string_representation(self):
        """Test method __unicode__"""
        request = Request(url='/', datetime='03/Oct/2018 13:19:45')
        self.assertEqual(unicode(request), u'03/Oct/2018 13:19:45 /')

    def test_fields_in_model(self):
        """Test all fields are represented in the model"""
        fields = {k.name: k.get_internal_type() for k in Request._meta.fields}
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
