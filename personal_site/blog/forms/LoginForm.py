from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.exceptions import ValidationError
from blog.models import BlogUser


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user is None:
                raise ValidationError('Špatný email nebo heslo.')

        return cleaned_data

    def login(self, request):
        try:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            user = authenticate(email=email, password=password)
        except KeyError:
            return None

        if user:
            auth_login(request, user)
            return user


    def is_valid(self, request):
        return super().is_valid() and self.login(request) is not None
