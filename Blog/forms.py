from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Community

class UserRegistrationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['first_name' , 'last_name' , 'email' , 'username', 'password1', 'password2']

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['CommunityName', 'Description']