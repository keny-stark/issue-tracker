from django import forms
from django.forms import widgets
from webapp.models import Type, Status


class TrackerForm(forms.Form):
    summary = forms.CharField(max_length=200, required=True, label='summary')
    description = forms.CharField(max_length=40, required=True, label='description', widget=widgets.Textarea)
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False, label='type', empty_label=None),
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False, label='status', empty_label=None)
