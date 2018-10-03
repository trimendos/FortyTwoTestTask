from json import dumps

from django.views.generic import TemplateView
from django.http import HttpResponse

from apps.hello.models import Profile


class MainPageView(TemplateView):
    template_name = 'hello/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        return context


class RequestsPageView(TemplateView):
    template_name = 'hello/requests_page.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            response = {
                'unviewed': 10,
                'webrequests': [{
                    'id': i,
                    'datetime': '03/Oct/2018 13:19:45',
                    'url': '/',
                    'method': 'GET',
                    'status_code': 200
                } for i in range(1, 11)
                ]
            }
            return HttpResponse(dumps(response))

        return super(RequestsPageView, self).get(request, *args, **kwargs)
