from os import path

from django.views.generic import TemplateView, ListView, UpdateView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from .models import Profile, Request
from .forms import ProfileUpdateForm, PriorityChangeForm
from .utils import json_response


class MainPageView(TemplateView):
    template_name = 'hello/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        return context


class RequestsPageView(ListView, FormView):
    template_name = 'hello/requests_page.html'
    model = Request
    form_class = PriorityChangeForm

    def get_queryset(self):
        return self.model.objects.order_by('-priority').values()[:10]

    def get(self, request, *args, **kwargs):
        raw_requests = Request.objects.values().order_by("-priority")[:10]
        if request.is_ajax():
            unviewed = self.model.get_unviewed_count()
            response = {'unviewed': unviewed}

            if unviewed:
                response['webrequests'] = list(raw_requests)

            return json_response(response)

        return super(RequestsPageView, self).get(request, *args, **kwargs)

    def form_invalid(self, form):
        return json_response({'errors': form.errors})

    def form_valid(self, form):
        cd = form.cleaned_data

        Request.update_priority(
            id=cd['rq_id'], priority=cd['priority']
        )
        return json_response({
            'webrequests': list(self.get_queryset()),
        })


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
