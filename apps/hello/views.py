from os import path

from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from .models import Profile, Request
from .forms import ProfileUpdateForm
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
            return json_response(response)

        return super(RequestsPageView, self).get(request, *args, **kwargs)


class ProfileUpdatePageView(UpdateView):
    model = Profile
    template_name = 'hello/update_profile_page.html'
    form_class = ProfileUpdateForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileUpdatePageView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('update_profile_page', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdatePageView, self).get_context_data(**kwargs)

        photo_exists = path.isfile(self.object.photo.path) \
            if self.object.photo else False

        context['photo_exists'] = photo_exists
        return context

    def form_invalid(self, form):
        response = super(ProfileUpdatePageView, self).form_invalid(form)
        if self.request.is_ajax():
            return json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(ProfileUpdatePageView, self).form_valid(form)
        if self.request.is_ajax():
            data = {'pk': self.object.pk}
            return json_response(data)
        else:
            return response
