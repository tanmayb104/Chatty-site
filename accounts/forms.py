from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Profile
from django import forms
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['user']