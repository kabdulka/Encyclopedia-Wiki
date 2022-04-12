from django import forms

class newEntryForm(forms.from):
    title = forms.CharField(label="wiki entry title", max_length=100)
    content = forms.CharField(label="Enter the content here", max_length=1000)