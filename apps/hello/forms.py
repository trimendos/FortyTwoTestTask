from datetime import date

from django.core.exceptions import ValidationError
from django import forms

from .models import Profile
from .widgets import DatePickerWidget


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
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control', 'data-minlength': 3, 'required': True}))
    last_name = forms.CharField(
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control', 'data-minlength': 3, 'required': True}))
    birthday = forms.DateField(
        validators=[validate_birthday],
        widget=DatePickerWidget(
            format="%d/%m/%Y",
            attrs={
                    'class': 'form-control',
                    'data-minlength': 3,
                    'required': True,
                    'data-birthday': 'birthday',
                    'autocomplete': 'off',
                    'pattern': '\d{1,2}/\d{1,2}/\d{4}'
            }
        ), input_formats=["%d/%m/%Y"])
    email = forms.EmailField(
        widget=forms.widgets.EmailInput(attrs={
            'class': 'form-control',
            'data-minlength': 3,
            'required': True,
            'pattern': '^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]'
                       '{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$',
            'data-required-error': 'This field is required.',
            'data-pattern-error': 'Enter a valid email address.'
        }))
    jabber = forms.CharField(
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control',
            'data-minlength': 3,
            'required': True,
            'pattern': '^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]'
                       '{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$',
            'data-required-error': 'This field is required.',
            'data-pattern-error': 'Enter a valid email address.'
        }))
    skype = forms.CharField(
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control', 'data-minlength': 3, 'required': True}))
    biography = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                'class': 'form-control',
                'cols': 40,
                'rows': 10
            }), required=False)
    contacts = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                'class': 'form-control',
                'cols': 40,
                'rows': 10
            }), required=False)

    class Meta:
        model = Profile
