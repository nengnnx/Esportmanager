from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class UserProfile(models.Model):
    username = models.CharField(max_length=100, null=True, blank=False)
    password = models.CharField(max_length=100, null=True, blank=False) 

class PlayerProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'ชาย'),
        ('female', 'หญิง'),
    ]

    member = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    player_name = models.CharField(max_length=100,  null=True, blank=False)
    game = models.CharField(max_length=100,  null=True, blank=False)
    name_lastname = models.CharField(max_length=100, null=True, blank=False)
    age = models.CharField(max_length=10, null=True, blank=False)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=False)
    province = models.CharField(max_length=100, null=True, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=False)
    facebook = models.CharField(max_length=100, null=True, blank=False)
    line = models.CharField(max_length=100, null=True, blank=False)
    description = models.TextField( null=True, blank=False)

    def __str__(self):
        return self.player_name

class WorkPicture(models.Model):
    player_profile = models.ForeignKey(PlayerProfile, related_name='work_pictures', on_delete=models.CASCADE,null=True, blank=False)
    image = models.ImageField(upload_to='work_pictures/', null=True, blank=False)

    def __str__(self):
        return f"Picture for {self.player_profile.player_name}"
    
#model team
class Game(models.Model):
    name = models.CharField(max_length=100, null=True, blank=False)
    rank1 = models.CharField(max_length=100, null=True, blank=False)
    rank2 = models.CharField(max_length=100,  null=True, blank=False)
    rank3 = models.CharField(max_length=100,  null=True, blank=False)
    rank4 = models.CharField(max_length=100,  null=True, blank=False)
    rank5 = models.CharField(max_length=100,  null=True, blank=False)
    rank6 = models.CharField(max_length=100,  null=True, blank=False)
    rank7 = models.CharField(max_length=100,  null=True, blank=False)
    rank8 = models.CharField(max_length=100, null=True, blank=False)
    rank9 = models.CharField(max_length=100,  null=True, blank=False)
    def __str__(self):
        return self.name

class Team(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    name = models.CharField(max_length=100, null=True, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=False)
    required_rank_min = models.CharField(max_length=100, null=True, blank=True)
    required_rank_max = models.CharField(max_length=100, null=True, blank=True)
    members_needed = models.IntegerField( null=True, blank=False)
    additional_details = models.TextField( null=True, blank=False)

    def __str__(self):
        return self.name  
    
class JoinRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='join_requests', null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    status = models.CharField(max_length=20, default='pending', null=True, blank=False)  
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return f"{self.user.username} -> {self.team.name} ({self.status})"
    
class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members', null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return f"{self.user.username} -> {self.team.name}"


