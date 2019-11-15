from django import forms
from webapp.models import Type, Status, Tracker, Project


class TrackerProjectForm(forms.ModelForm):
    class Meta:
        model = Tracker

        widgets = {
            'summary': forms.TextInput,
        }
        exclude = ['created_at', 'created_by', 'project_id']


class TrackerForm(forms.ModelForm):
    class Meta:
        model = Tracker
        widgets = {
            'summary': forms.TextInput,
        }
        fields = ['summary', 'description', 'type', 'status', 'project_id']
        exclude = ['created_at']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'status']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['type']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")
