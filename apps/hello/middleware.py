from django.core.urlresolvers import reverse
from .models import Request


class RequestMiddleware(object):

    def process_response(self, request, response):
        is_requests_page = request.path == reverse('requests_page')

        if not request.is_ajax():
            Request.objects.create(method=request.method,
                                   url=request.path,
                                   status_code=response.status_code,
                                   viewed=is_requests_page)
        return response
