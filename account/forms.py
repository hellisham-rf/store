from django.forms import Form, ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import User
from django.contrib.auth.forms import AuthenticationForm
class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    pass
