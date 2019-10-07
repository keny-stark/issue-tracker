from django import forms
from webapp.models import Type, Status, Tracker


class TrackerForm(forms.ModelForm):
    class Meta:
        model = Tracker
        widgets = {
            'summary': forms.TextInput
        }
        exclude = ['created_at']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['type']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status']
