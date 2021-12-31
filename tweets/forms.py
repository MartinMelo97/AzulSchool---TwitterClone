from django import forms
from .models import Tweet

class CreateTweetForm(forms.ModelForm):

    body = forms.CharField(
        widget=forms.Textarea(),
        label='¿Qué está pasando?'
    )
    class Meta:
        model = Tweet
        fields = ['body']