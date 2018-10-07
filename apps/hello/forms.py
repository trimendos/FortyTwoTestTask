from datetime import date

from django.core.exceptions import ValidationError
from django import forms

from .models import Profile


BOOTS_ATTRS = {'class': 'form-control'}


def validate_birthday(value):
    today = date.today()
    max_age = today.year - date(1940, 1, 1).year
    max_date = date(
        today.year - max_age, today.month, today.day)
    if value <= max_date or value >= date.today():
        raise ValidationError(
            'Date should be younger than today and not older '
            'than {} years'.format(max_age)
        )


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    last_name = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    birthday = forms.DateField(
        validators=[validate_birthday],
        input_formats=['%B %d, %Y'])
    email = forms.EmailField(
        widget=forms.widgets.EmailInput(attrs=BOOTS_ATTRS))
    jabber = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    skype = forms.CharField(
        widget=forms.widgets.TextInput(attrs=BOOTS_ATTRS))
    biography = forms.CharField(
        widget=forms.widgets.Textarea(attrs=BOOTS_ATTRS), required=False),
    contacts = forms.CharField(
        widget=forms.widgets.Textarea(attrs=BOOTS_ATTRS), required=False)

    class Meta:
        model = Profile
