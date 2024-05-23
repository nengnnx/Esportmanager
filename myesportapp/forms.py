# myesportapp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm  # Import the built-in form
from django.contrib.auth import logout
from .models import PlayerProfile, WorkPicture
from .models import Team

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField( max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = [
            'player_name', 'game', 'name_lastname', 'age', 'gender',
            'province', 'phone_number', 'facebook', 'line', 'description'
        ]
        widgets = {
            'gender': forms.RadioSelect(choices=PlayerProfile.GENDER_CHOICES),
        }

class WorkPictureForm(forms.ModelForm):
    class Meta:
        model = WorkPicture
        fields = ['image']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'game', 'required_rank_min', 'required_rank_max', 'members_needed', 'additional_details']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 p-2 w-full border rounded-md'}),
            'game': forms.Select(attrs={'class': 'mt-1 p-2 w-full border rounded-md'}),
            'required_rank_min': forms.Select(attrs={'class': 'mt-1 p-2 w-full border rounded-md'}),
            'required_rank_max': forms.Select(attrs={'class': 'mt-1 p-2 w-full border rounded-md'}),
            'members_needed': forms.NumberInput(attrs={'class': 'mt-1 p-2 w-full border rounded-md'}),
            'additional_details': forms.Textarea(attrs={'class': 'mt-1 p-2 w-full border rounded-md'}),
        }