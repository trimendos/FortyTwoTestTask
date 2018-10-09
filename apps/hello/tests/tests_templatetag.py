from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Profile


class TestTagEditLink(TestCase):
    """Test  custom tag "edit_link"."""
    TEMPLATE = Template('{% load custom_tags %}{% edit_link profile %}')

    def test_valid_object(self):
        """Return url to the admin edit page of the passed object"""
        profile = Profile.objects.first()
        expected_url = 'admin/hello/profile/1'
        rendered_url = self.TEMPLATE.render(Context({'profile': profile}))
        self.assertIn(
            expected_url,
            rendered_url,
            'Returned url != Expected url\n\r{} != {}'.format(
                rendered_url, expected_url
            )
        )

    def test_invalid_object(self):
        """Should raise the TemplateSyntaxError exception"""
        with self.assertRaises(TemplateSyntaxError):
            self.TEMPLATE.render(Context({'profile': 1}))

    def test_link_on_main_page(self):
        """Test link there is at the main page"""
        response = self.client.get(reverse('main_page'))
        self.assertContains(response, '/admin/hello/profile/1/')
