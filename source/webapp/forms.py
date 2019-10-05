from django import forms
from webapp.models import Type, Status, Tracker


# class TrackerForm(forms.Form):
#     summary = forms.CharField(max_length=100, required=True, label='summary')
#     description = forms.CharField(max_length=2000, required=False, label='description', widget=widgets.Textarea)
#     type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False, label='type', empty_label=None)
#     status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False, label='status', empty_label=None)

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



#
# class TypeForm(forms.Form):
#     type = forms.CharField(max_length=40, required=True, label=type)
#
#
# class StatusForm(forms.Form):
#     status = forms.CharField(max_length=40, required=True, label=type)
