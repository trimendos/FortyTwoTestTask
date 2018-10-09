from django.test import TestCase
from django.core.urlresolvers import reverse


class DatePickerWidgetTest(TestCase):
    """Test DatePickerWidget is in the template"""
    def test_birthday_widget(self):
        """Template should contains custom widget"""
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('update_profile_page',
                                           kwargs={'pk': 1}))
        self.assertContains(response, '//code.jquery.com/ui/1.12.1/'
                                      'themes/base/jquery-ui.css')
        self.assertContains(response, 'https://code.jquery.com/ui/1.12.1/'
                                      'jquery-ui.js')
        self.assertContains(response, 'CalendarWidget/js/datepicker.js')
