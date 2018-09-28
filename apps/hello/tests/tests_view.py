from django.test import TestCase
from django.core.urlresolvers import reverse


DATA = {
    'first_name': 'Roman',
    'last_name': 'Duz',
    'birthday': 'July 7, 1990',
    'email': 'admin@mail.com',
    'jabber': 'trimendos@jabber.ru',
    'skype': 'keni-voni-be',
    'biography': 'Have 5+ years of overall experience in IT including '
                 'technical support, QA automation, etc. \r\n'
                 'Experience with Python, PHP, CMD, Bash Scripting, Linux, '
                 'Web Development (JQuery, HTML, CSS)',
    'contacts': 'tel. +38(093)683-40-96'
}


class MainPageTest(TestCase):
    def setUp(self):
        self.url = reverse('main_page')
        self.response = self.client.get(self.url)

    def test_page_returned(self):
        """Test main page is returned"""
        self.assertEqual(self.response.status_code, 200,
                         'Page was not returned')
        self.assertContains(self.response, 'Profile')
        self.assertTemplateUsed(self.response, 'hello/main_page.html')
        self.assertEqual(self.response.context['profile'], DATA)
