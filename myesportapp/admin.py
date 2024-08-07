from django.contrib import admin

# Register your models here.
from .models import *  # Import your model
admin.site.register(UserProfile)  # Register your model
admin.site.register(PlayerProfile) 
admin.site.register(WorkPicture) 
admin.site.register(JoinRequest)
admin.site.register(Game)
admin.site.register(Team)
admin.site.register(TeamMember)

from myesportapp.forms import *