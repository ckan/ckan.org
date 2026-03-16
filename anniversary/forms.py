from django import forms


class GetInvolvedForm(forms.Form):
    FNAME = forms.CharField(max_length=100, required=True)
    ORG = forms.CharField(max_length=100, required=False)
    EMAIL = forms.EmailField(required=True)
    CKANUSE = forms.CharField(max_length=100, required=False)
    MESSAGE = forms.CharField(widget=forms.Textarea, required=False)
    