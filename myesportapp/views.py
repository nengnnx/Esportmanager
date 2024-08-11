# myesportapp/views.py
from audioop import reverse
from cProfile import Profile
from collections import UserDict, UserList
from contextlib import redirect_stderr, redirect_stdout
from django.shortcuts import render , redirect ,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *   
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from .forms import GameForm
from django.db.models import F
from django.db.models import Count
from myesportapp.forms import RegistrationForm
from django.db.models import Case, When, IntegerField, F
from django.forms import inlineformset_factory

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home') 

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('foradmin')
                else:
                    return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def profile(req):
    return render(req,'prifile.html')

def search(req):
    return render(req,'search.html')

def navbar(req):
    return render(req,'navbar.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def create_profile(request):
    WorkPictureFormSet = modelformset_factory(WorkPicture, form=WorkPictureForm, extra=3)

    if request.method == 'POST':
        profile_form = PlayerProfileForm(request.POST, request.FILES)
        formset = WorkPictureFormSet(request.POST, request.FILES, queryset=WorkPicture.objects.none())

        if profile_form.is_valid() and formset.is_valid():
            player_profile = profile_form.save(commit=False)
            player_profile.member = request.user
            player_profile.save()

            for form in formset.cleaned_data:
                if form:
                    image = form.get('image')
                    if image:
                        WorkPicture(player_profile=player_profile, image=image).save()

            return redirect('profile')
        else:
            print(profile_form.errors)
            print(formset.errors)
    else:
        profile_form = PlayerProfileForm()
        formset = WorkPictureFormSet(queryset=WorkPicture.objects.none())

    return render(request, 'profile.html', {'profile_form': profile_form, 'formset': formset})


@login_required
def profile_detail(request):
    profiles = PlayerProfile.objects.filter(member=request.user)

    profile_pictures = {}
    for profile in profiles:
        profile_pictures[profile.id] = WorkPicture.objects.filter(player_profile=profile)
    
    return render(request, 'profile_detail.html', {
        'profiles': profiles,
        'profile_pictures': profile_pictures
    })


@login_required
def edit_profile(request, profile_id):
    profile = get_object_or_404(PlayerProfile, id=profile_id)
    WorkPictureFormSet = inlineformset_factory(PlayerProfile, WorkPicture, form=WorkPictureForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, instance=profile)
        formset = WorkPictureFormSet(request.POST, request.FILES, instance=profile)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save() 
            return redirect('profile_detail')
    else:
        form = PlayerProfileForm(instance=profile)
        formset = WorkPictureFormSet(instance=profile)

    return render(request, 'edit_profile.html', {'form': form, 'formset': formset})

def work_pictures_list(request):
    if request.method == 'POST':
        form = WorkPictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('work_pictures_list')  
    else:
        form = WorkPictureForm()  

    pictures = WorkPicture.objects.all() 
    return render(request, 'work_pictures_list.html', {'pictures': pictures, 'form': form})

def delete_work_picture(request, picture_id):
    picture = get_object_or_404(WorkPicture, id=picture_id)
    profile_id = picture.player_profile.id 
    picture.delete()
    return redirect('edit_profile', profile_id=profile_id)

def delete_profile(request, profile_id):
    profile = get_object_or_404(PlayerProfile, id=profile_id, member=request.user)
    if request.method == 'POST':
        profile.delete()
        return redirect('profile_detail')  
    return render(request, 'profile_detail.html', {'profile': profile})

@login_required
def some_view(request):
    user = request.user
    has_profile = False
    if user.is_authenticated:
        has_profile = PlayerProfile.objects.filter(user=user).exists()
    
    return render(request, 'myesportapp/components/navbar.html', {'has_profile': has_profile})

@login_required
def create_team(request):
    selected_game = None

    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.member = request.user
            team.save()
            return redirect('my_team')
    else:
        form = TeamForm()
        if 'game' in request.GET:
            try:
                game_id = int(request.GET['game'])
                selected_game = Game.objects.get(id=game_id)
                form.fields['required_rank_min'].choices = form.get_rank_choices(selected_game)
                form.fields['required_rank_max'].choices = form.get_rank_choices(selected_game)
                form.initial['game'] = selected_game
            except (ValueError, TypeError, Game.DoesNotExist):
                selected_game = None

    return render(request, 'create_team.html', {'form': form, 'selected_game': selected_game})

@login_required
def create_game(req):
    return render(req,'create_game_admin.html')

def my_team(request):
    current_user = request.user
    teams = (Team.objects.filter(members__user=current_user) | 
             Team.objects.filter(member=current_user)).distinct()
    for team in teams:
        member_count = team.members.count()
        team.total_members = member_count

    context = {
        'teams': teams,
    }
    return render(request, 'my_team.html', context)

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'home.html', {'teams': teams})

def foradmin(req):
    return render(req,'foradmin.html')

def add_game(request):
    if request.method == 'POST':

        try:
            name = request.POST.get('name')
            rank1 = request.POST.get('rank1')
            rank2 = request.POST.get('rank2')
            rank3 = request.POST.get('rank3')
            rank4 = request.POST.get('rank4')
            rank5 = request.POST.get('rank5')
            rank6 = request.POST.get('rank6')
            rank7 = request.POST.get('rank7')
            rank8 = request.POST.get('rank8')
            rank9 = request.POST.get('rank9')
            number_of_players = request.POST.get('number_of_players')

            game = Game(
                name=name,
                rank1=rank1,
                rank2=rank2,
                rank3=rank3,
                rank4=rank4,
                rank5=rank5,
                rank6=rank6,
                rank7=rank7,
                rank8=rank8,
                rank9=rank9,
                number_of_players=number_of_players
            )
            game.save()
            print(game)
            return redirect('success_page')
        
        except Exception as e:
            print(f"{e}")

    return render(request, 'create_game_admin.html')

def game_list(request):
    games = Game.objects.all()
    return render(request, 'game_list.html', {'games': games})

def edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_list')
    else:
        form = GameForm(instance=game)
    return render(request, 'edit_game.html', {'form': form})

def team_detail_view(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'team_detail.html', {'team': team})

@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if team.member == request.user:
        messages.error(request, "You cannot join a team you lead.")
        return redirect('home')
    
    user_teams = TeamMember.objects.filter(user=request.user)
    if user_teams.exists():
        messages.error(request, "You are already a member of a team.")
        return redirect('home')

    profile_id = request.POST.get('player_profile')
    profile = get_object_or_404(PlayerProfile, id=profile_id)

    join_request, created = JoinRequest.objects.get_or_create(team=team, user=request.user, profile=profile)

    return redirect('my_team')


@login_required
def join_requests(request):
    # Filter join requests to show only those for teams where the current user is the leader
    join_requests = JoinRequest.objects.filter(team__member=request.user, status='pending')
    
    # Check if the user is already a member of a team
    user_has_team = TeamMember.objects.filter(user=request.user).exists()
    
    return render(request, 'join_request.html', {
        'join_requests': join_requests,
        'user_has_team': user_has_team
    })


def accept_join_request(request, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id)
    team = join_request.team
    user = join_request.user

    if team.member != request.user:
        return redirect('join_requests')

    if TeamMember.objects.filter(user=user, team__game=team.game).exists():
        return render(request, 'join_request.html', {
            'error_message': f'ผู้เล่นนี้มีทีมอยู่แล้วในเกม {team.game} และไม่สามารถส่งคำขอเข้าร่วมทีมใหม่ได้',
            'join_requests': JoinRequest.objects.filter(team__member=request.user, status='pending')
        })
    
    if join_request.status in ['approved', 'rejected']:
        return redirect('join_requests')

    if TeamMember.objects.filter(user=user, team__game=team.game).exists():
        return redirect('join_requests')

    join_request.status = 'approved'
    join_request.save()

    TeamMember.objects.create(team=team, user=user)
    
    join_request.delete()
    return redirect('join_requests')

def reject_join_request(request, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id)
    join_request.status = 'rejected'
    join_request.delete()
    
    return redirect('join_requests')

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    member_count = team.members.count()
    total_members = member_count

    context = {
        'team': team,
        'total_members': total_members,
    }
    return render(request, 'team_detail.html', context)

def user_profile(request, user_id):
    player_profile = get_object_or_404(PlayerProfile, member_id=user_id)
    return render(request, 'user_profile.html', {'player_profile': player_profile})


def team_list(request):
    games = Game.objects.all()
    teams = Team.objects.annotate(
        member_count=Count('members')
    )

    # สร้าง rank_choices จากข้อมูลในฐานข้อมูล
    rank_choices = {}
    for game in games:
        rank_choices[game.name.lower()] = {
            game.rank1: 1,
            game.rank2: 2,
            game.rank3: 3,
            game.rank4: 4,
            game.rank5: 5,
            game.rank6: 6,
            game.rank7: 7,
            game.rank8: 8,
            game.rank9: 9
        }

    game_name = request.GET.get('gameName')
    rank_min = request.GET.get('rankMin')
    rank_max = request.GET.get('rankMax')

    selected_game = Game.objects.filter(id=game_name).first() if game_name else None

    if selected_game:
        teams = teams.filter(game=selected_game)
        
        game_key = selected_game.name.lower()
        ranks = rank_choices.get(game_key, {})

        # รับค่าแรงค์เป็นตัวเลข
        rank_min_value = ranks.get(rank_min)
        rank_max_value = ranks.get(rank_max)

        if rank_min_value is not None and rank_max_value is not None:
            # แปลงค่าของแรงค์เป็นตัวเลขสำหรับการกรอง
            teams = teams.annotate(
                rank_min_numeric=Case(
                    *[When(required_rank_min=rank, then=value) for rank, value in ranks.items()],
                    output_field=IntegerField()
                ),
                rank_max_numeric=Case(
                    *[When(required_rank_max=rank, then=value) for rank, value in ranks.items()],
                    output_field=IntegerField()
                )
            ).filter(
                rank_min_numeric__lte=rank_max_value,
                rank_max_numeric__gte=rank_min_value
            )

            # กรองทีมที่มี rank_min >= rank_min_value
            teams = teams.filter(rank_min_numeric__gte=rank_min_value)

    # กรองทีมที่มีจำนวนสมาชิกไม่พอ
    teams = teams.filter(member_count__lt=F('members_needed')).distinct()

    return render(request, 'home.html', {
        'teams': teams,
        'games': games,
        'rank_choices': rank_choices,
        'selected_game': selected_game,
        'selected_rank_min': rank_min,
        'selected_rank_max': rank_max,
    })


def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    if team.member == request.user:
        team.delete()
        
    else:
        team_member = TeamMember.objects.filter(team=team, user=request.user).first()
        if team_member:
            team_member.delete()
            JoinRequest.objects.filter(team=team, user=request.user).delete()
        else:
            messages.error(request, "You are not a member of this team.")
    
    return redirect('home')