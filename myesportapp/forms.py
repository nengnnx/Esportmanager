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
from .models import *

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
    game = forms.ModelChoiceField(queryset=Game.objects.all(), empty_label="Select Game")
    required_rank_min = forms.ChoiceField(choices=[], required=False)
    required_rank_max = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = Team
        fields = ['name', 'game', 'required_rank_min', 'required_rank_max', 'members_needed', 'additional_details']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'game' in self.data:
            try:
                game_id = int(self.data.get('game'))
                game = Game.objects.get(id=game_id)
                self.fields['required_rank_min'].choices = self.get_rank_choices(game)
                self.fields['required_rank_max'].choices = self.get_rank_choices(game)
            except (ValueError, TypeError, Game.DoesNotExist):
                pass
        elif self.instance.pk:
            game = self.instance.game
            self.fields['required_rank_min'].choices = self.get_rank_choices(game)
            self.fields['required_rank_max'].choices = self.get_rank_choices(game)

    def get_rank_choices(self, game):
        ranks = []
        for rank in range(1, 10):
            rank_field = f'rank{rank}'
            rank_value = getattr(game, rank_field, None)
            if rank_value:
                ranks.append((rank_value, rank_value))
        return ranks