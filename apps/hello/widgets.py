from django import forms


class DatePickerWidget(forms.DateInput):

    class Media:
        js = ('CalendarWidget/js/datepicker.js',)

    def __init__(self, format=None, attrs=None):
        if format is None:
            format = '%d/%m/%Y'
        if attrs is None:
            attrs = {
                'class': 'calendar-widget',
                'placeholder': 'Month dd, yyyy'
            }
        super(DatePickerWidget, self).__init__(format=format, attrs=attrs)
