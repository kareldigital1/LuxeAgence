from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your models here.

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        )
    password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
