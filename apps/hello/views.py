from django.views.generic import TemplateView


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


class MainPage(TemplateView):
    template_name = 'hello/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context['profile'] = DATA
        return context
