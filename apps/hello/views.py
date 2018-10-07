from django.views.generic import TemplateView, ListView, UpdateView
from django.http import HttpResponse

from apps.hello.models import Profile, Request
from .utils import json_response


class MainPageView(TemplateView):
    template_name = 'hello/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        return context


class RequestsPageView(ListView):
    template_name = 'hello/requests_page.html'
    model = Request
    queryset = Request.objects.values()[:10]

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.GET.get('infocus') == 'true':
                Request.objects.filter(viewed=False).update(viewed=True)

            raw_requests = Request.objects.values()[:10]
            response = {
                'unviewed': self.model.get_unviewed_count(),
                'webrequests': list(raw_requests)
            }
            return HttpResponse(json_response(response),
                                content_type="application/json")

        return super(RequestsPageView, self).get(request, *args, **kwargs)


class ProfileUpdatePageView(UpdateView):
    pass
