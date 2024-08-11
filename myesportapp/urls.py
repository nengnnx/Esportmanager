from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', team_list, name='team_list'),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('search/', search, name='search'),
    path('navbar/', navbar, name='navbar'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('my_team/', my_team, name='my_team'),
    path('profile/', create_profile, name='profile'),
    path('profile_detail/', profile_detail, name='profile_detail'),
    #path('profile/edit/<int:profile_id>', edit_profile, name='edit_profile'),
    path('profile/delete/<int:profile_id>/', delete_profile, name='delete_profile'),
    path("navbar",some_view,name='some_view'),
    path('create_game_admin/', create_game, name='create_game'),
    path('create_team/',create_team,name='create_team'),
    path('create_game_admnin/', add_game, name='add_game'),
    path('foradmin',foradmin,name='foradmin'),
    path('game_list',game_list, name='game_list'),
    path('edit/<int:game_id>/',edit_game, name='edit_game'),
    path('join_team/<int:team_id>/', join_team, name='join_team'),
    path('join_request/', join_requests, name='join_requests'),
    path('accept_join_request/<int:request_id>/', accept_join_request, name='accept_join_request'),
    path('reject_join_request/<int:request_id>/', reject_join_request, name='reject_join_request'),
    path('team/<int:pk>/', team_detail, name='team_detail'),
    path('user_profile/<int:user_id>/', user_profile, name='user_profile'),
    path('leave_team/<int:team_id>/', leave_team, name='leave_team'),
    path('edit_profile/<int:profile_id>/', edit_profile, name='edit_profile'),
    path('edit_profile/work_pictures/', work_pictures_list, name='work_pictures_list'),
    path('delete_work_picture/<int:picture_id>/', delete_work_picture, name='delete_work_picture'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
