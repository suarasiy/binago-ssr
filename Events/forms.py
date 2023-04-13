from django import forms
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError
from .models import Events, EventsCategories

import datetime
import pytz


class EventForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'input__field', 'placeholder': 'Write your event title',
               'spellcheck': 'false', 'id': 'title', 'autocomplete': 'off'}
    ))
    category = forms.ModelChoiceField(queryset=EventsCategories.objects.all().order_by('category'), widget=forms.Select(attrs={
        'placehlder': 'Choose category', 'id': 'category', 'placeholder': 'Event Category'
    }))
    max_audience = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'input__field', 'placeholder': 'Total max audience / seat',
               'min': '0', 'id': 'max-audience', 'autocomplete': 'off'}
    ))
    banner = forms.ImageField(
        allow_empty_file=False, required=True, widget=forms.ClearableFileInput(
            attrs={'id': 'banner', 'class': 'input__field__file', 'accept': 'image/*'}
        )
    )
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'input__field', 'placeholder': 'Set it to 0 if it\'s free',
               'min': '0', 'id': 'fee', 'autocomplete': 'off'}
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input__field min__h__50px', 'placeholder': 'Describe abour your events...',
               'rows': '8', 'spellcheck': 'false', 'id': 'description', 'autocomplete': 'off'}
    ))
    # schedule_start = forms.DateTimeField(widget=DateTimeInput(
    #     attrs={'class': 'input__field', 'placeholder': 'Schedule to start', 'id': 'schedule-start'}
    # ))
    # schedule_end = forms.DateTimeField(widget=DateTimeInput(
    #     attrs={'class': 'input__field', 'placeholder': 'Schedule to start', 'id': 'schedule-end'}
    # ))
    schedule_start = forms.DateTimeField(widget=forms.TextInput(
        attrs={'class': 'input__field', 'placeholder': 'Schedule to start',
               'id': 'schedule-start', 'type': 'datetime-local'}
    ))
    schedule_end = forms.DateTimeField(widget=forms.TextInput(
        attrs={'class': 'input__field', 'placeholder': 'Schedule to start',
               'id': 'schedule-end', 'type': 'datetime-local'}
    ))
    url_stream = forms.URLField(max_length=500, widget=forms.TextInput(
        attrs={'class': 'input__field', 'placeholder': 'Put your url stream',
               'spellcheck': 'false', 'id': 'url-stream', 'autocomplete': 'off'}
    ))
    url_homepage = forms.URLField(max_length=500, widget=forms.TextInput(
        attrs={'class': 'input__field',
               'placeholder': 'Put your event reference (optional)', 'spellcheck': 'false', 'id': 'url-homepage', 'autocomplete': 'off'}
    ))

    def clean_schedule_start(self):
        data = self.cleaned_data["schedule_start"]
        _datetime = data.replace(tzinfo=pytz.UTC)
        now = datetime.datetime.today().replace(tzinfo=pytz.UTC)
        if _datetime < now:
            raise ValidationError("The start schedule cannot be past time.")
        return data

    def clean_schedule_end(self):
        data = self.cleaned_data["schedule_end"]
        _datetime = data.replace(tzinfo=pytz.UTC)
        now = datetime.datetime.today().replace(tzinfo=pytz.UTC)
        if _datetime < now:
            raise ValidationError("The end schedule cannot be past time.")
        return data

    def clean(self):
        cleaned_data = super().clean()
        schedule_start = cleaned_data.get('schedule_start', None)
        schedule_end = cleaned_data.get('schedule_end', None)
        if schedule_start and schedule_end:
            if schedule_end.replace(tzinfo=pytz.UTC) < schedule_start.replace(tzinfo=pytz.UTC):
                raise ValidationError("The end schedule of event cannot be exact same from start event.")

        return super().clean()

    def clean_max_audience(self):
        data = self.cleaned_data["max_audience"]
        if data < 0:
            raise ValidationError("The number of audience must be a positive.")
        return data

    def clean_price(self):
        data = self.cleaned_data["price"]
        if data < 0:
            raise ValidationError("The number should not less than 0.")
        if data >= 1 and data < 20000:
            raise ValidationError("The price should not be less than 20,000. Set it to 0 If it's free.")
        return data

    class Meta:
        model = Events
        fields = ['title', 'banner', 'category', 'price', 'description', 'max_audience',
                  'schedule_start', 'schedule_end', 'url_stream', 'url_homepage']


class EventEditForm(EventForm):

    schedule_start = None
    schedule_end = None

    def clean_schedule_start(self):
        ...

    def clean_schedule_end(self):
        ...

    def clean(self):
        ...

    class Meta:
        model = Events
        fields = ['title', 'banner', 'category', 'price', 'description', 'max_audience',
                  'url_stream', 'url_homepage']


class EventsCoverageForm(forms.Form):
    coverage = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input__field', 'placeholder': 'Add topics that covered... *separate with ||',
               'spellcheck': 'false', 'id': 'coverage', 'autocomplete': 'off'}
    ))
