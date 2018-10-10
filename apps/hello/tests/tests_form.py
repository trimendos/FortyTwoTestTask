from datetime import date
from factory import fuzzy, DjangoModelFactory, LazyAttribute, Faker

from django.test import TestCase

from ..models import Profile
from ..forms import ProfileUpdateForm, PriorityChangeForm
from ..utils import years_ago


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    birthday = fuzzy.FuzzyDate(date(1940, 1, 1), date.today() - years_ago(16))
    email = Faker('email')
    jabber = Faker('email')
    skype = LazyAttribute(lambda o: '%s.%s' % (o.first_name, o.last_name))
    biography = fuzzy.FuzzyText(length=50)
    contacts = fuzzy.FuzzyText(length=50)


class ProfileUpdateFormTest(TestCase):
    def setUp(self):
        self.form = ProfileUpdateForm

    def test_update_form_valid_data(self):
        """Test update profile instance with valid data"""
        profile = Profile.objects.first()
        new_data = ProfileFactory.build(id=1).__dict__
        form = self.form(new_data, instance=profile)
        self.assertTrue(form.is_valid())
        form.save()

        for field in profile._meta.get_all_field_names():
            value = getattr(profile, field)
            if field is not 'photo':
                self.assertEqual(value, form.data[field])

    def test_update_form_with_blank_data(self):
        """Test update profile instance with blank data"""
        profile = Profile.objects.first()
        form = self.form(data={}, instance=profile)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {
            'first_name': [u'This field is required.'],
            'last_name': [u'This field is required.'],
            'birthday': [u'This field is required.'],
            'email': [u'This field is required.'],
            'jabber': [u'This field is required.'],
            'skype': [u'This field is required.'],
        })

    def test_validate_date(self):
        """The input data are the boundary values of the age."""
        too_old = ProfileFactory.build(id=1,
                                       birthday=date(1777, 1, 1)).__dict__
        self.assertFalse(
            self.form(data=too_old).is_valid(),
            "The age is too old")

        too_young = ProfileFactory.build(id=1,
                                         birthday=date.today()).__dict__
        self.assertFalse(
            self.form(data=too_young).is_valid(),
            "The age is too young"
        )

        normal = ProfileFactory.build(id=1).__dict__
        self.assertTrue(
            self.form(data=normal).is_valid(),
            "The date is incorrect"
        )


class PriorityChangeFormTest(TestCase):

    def test_valid_form(self):
        """Valid case"""
        form = PriorityChangeForm(data={
            'rq_id': 1,
            'priority': 1
        })
        self.assertTrue(form.is_valid())

    def test_non_valid_form_priority_is_negative(self):
        """Non valid case, priority can't be a negative number"""
        form = PriorityChangeForm(data={
            'rq_id': 1,
            'priority': -1
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['priority'],
            ['Ensure this value is greater than or equal to 0.']
        )

    def test_non_valid_form_priority_is_too_high(self):
        """Non valid case, priority is highest then 999"""
        form = PriorityChangeForm(data={
            'rq_id': 1,
            'priority': 1000
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['priority'],
            ['Ensure this value is less than or equal to 999.']
        )

    def test_empty_fields(self):
        """All fields is required"""
        form = PriorityChangeForm(data={})
        err_msg = ['This field is required.']
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['rq_id'], err_msg)
        self.assertEqual(form.errors['priority'], err_msg)
