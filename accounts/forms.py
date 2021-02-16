from django import forms
from .models import TwitterUser

class UserForm(forms.ModelForm):
    date_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1950, 2011)),
        label='Fecha de nacimiento'
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'email-input'}),
        label='Correo electrónico'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Contraseña'
    )

    class Meta:
        model = TwitterUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'date_birth',
            'email',
            'password'
        )