from django import forms
from webapp.models import Type, Status, Tracker, Project


class TrackerForm(forms.ModelForm):
    class Meta:
        model = Tracker
        widgets = {
            'summary': forms.TextInput,
            'project_id': forms.ChoiceField(required=True)
        }
        exclude = ['created_at']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'created_at', 'updated_at']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['type']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status']
