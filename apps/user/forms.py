from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django_registration.forms import RegistrationFormUniqueEmail

from apps.user.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class SignupForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    birth_date = forms.DateField(widget=DateInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'birth_date')


class SigninForm(forms.Form):
    email = forms.EmailField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')
