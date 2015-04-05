from django import forms

class formOptions(forms.Form):
    inipv6address = forms.CharField(max_length=128)
