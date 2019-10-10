from django import forms
from webapp.models import Type, Status, Tracker, Project


class TrackerForm(forms.ModelForm):
    class Meta:
        model = Tracker

        widgets = {
            'summary': forms.TextInput,
        }
        exclude = ['created_at']


class TrackerProjectForm(forms.ModelForm):
    class Meta:
        model = Tracker
        widgets = {
            'summary': forms.TextInput,
        }
        fields = ['summary', 'description', 'type', 'status']
        exclude = ['created_at', 'project_id']



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
