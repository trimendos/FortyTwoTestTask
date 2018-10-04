import decimal
import datetime
from json import dumps

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils.timezone import is_aware


class DjangoOverRideJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%d/%b/%Y %H:%M:%S")
        elif isinstance(o, datetime.date):
            return o.strftime("%d/%b/%Y")
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            return o.strftime("%H:%M:%S")
        elif isinstance(o, decimal.Decimal):
            return str(o)
        return super(DjangoOverRideJSONEncoder, self).default(o)


def json_response(response):
    return HttpResponse(
        dumps(response, cls=DjangoOverRideJSONEncoder),
        content_type="application/json")
