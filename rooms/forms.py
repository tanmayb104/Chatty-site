
from .models import Room, Message
from django import forms

class CreateRoomForm(forms.ModelForm):

    class Meta:
        model = Room
        exclude = ['code','participants']
