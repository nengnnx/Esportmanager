from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    #path('profile/', profile, name='profile'),
    path('search/', search, name='search'),
    path('navbar/', navbar, name='navbar'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('my_team/', my_team, name='my_team'),
    path('profile/', create_profile, name='profile'),
    path('profile_detail/', profile_detail, name='profile_detail'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path("navbar",some_view,name='some_view'),
    path('create_game_admin/', create_game, name='create_game'),
    path('create_team/',create_team,name='create_team'),
    path('create_game_admnin/', add_game, name='add_game'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
