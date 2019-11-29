from django import forms
from webapp.models import Type, Status, Tracker, Project
from django.contrib.auth.models import User


class TrackerProjectForm(forms.ModelForm):
    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        self.fields['assigned_to'].queryset = user

    class Meta:
        model = Tracker

        widgets = {
            'summary': forms.TextInput,
        }
        exclude = ['created_at', 'created_by', 'project_id']


class ProjectForm(forms.ModelForm):
    def __init__(self, users=None, **kwargs):
        super().__init__(**kwargs)
        self.fields['users'] = forms.ModelMultipleChoiceField(queryset=users)

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
