from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def edit_link(obj):
    """A template tag accepts any object and renders a link to its admin edit
    page"""
    try:
        view_name = 'admin:{}_change'.format(obj._meta.db_table)
        return reverse(view_name, args=(obj.pk,))
    except AttributeError:
        raise template.TemplateSyntaxError(
            "{} isn't correct object".format(obj))
