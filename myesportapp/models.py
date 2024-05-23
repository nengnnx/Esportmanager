from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100) 

class PlayerProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'ชาย'),
        ('female', 'หญิง'),
    ]

    member = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    player_name = models.CharField(max_length=100, null=True)
    game = models.CharField(max_length=100, null=True)
    name_lastname = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True)
    province = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    facebook = models.CharField(max_length=100, null=True)
    line = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.player_name

class WorkPicture(models.Model):
    player_profile = models.ForeignKey(PlayerProfile, related_name='work_pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='work_pictures/', null=True, blank=True)

    def __str__(self):
        return f"Picture for {self.player_profile.player_name}"
    
#model team
class Rank(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    ranks = models.ManyToManyField(Rank, related_name='games')
    number_of_players = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    required_rank_min = models.ForeignKey(Rank, related_name='team_min_ranks', on_delete=models.SET_NULL, null=True)
    required_rank_max = models.ForeignKey(Rank, related_name='team_max_ranks', on_delete=models.SET_NULL, null=True)
    members_needed = models.IntegerField(null=False, blank=False)
    additional_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
        