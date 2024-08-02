# myesportapp/views.py
from audioop import reverse
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

def profile(request):
    return render(request, 'profile.html')

@login_required
def profile_detail(request):
    try:
        player_profile = PlayerProfile.objects.get(member=request.user)
        work_pictures = WorkPicture.objects.filter(player_profile=player_profile)
        has_profile = True
    except PlayerProfile.DoesNotExist:
        has_profile = False

    return render(request, 'profile_detail.html', {
        'has_profile': has_profile,
        'player_profile': player_profile if has_profile else None,
        'work_pictures': work_pictures if has_profile else None
    })


@login_required
def edit_profile(request):
    player_profile = get_object_or_404(PlayerProfile, member=request.user)
    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, instance=player_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = PlayerProfileForm(instance=player_profile)
    
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def some_view(request):
    has_profile = PlayerProfile.objects.filter(member=request.user).exists()
    return render(request, 'profile_detail.html', {'has_profile': has_profile})

@login_required
def create_team(request):
    selected_game = None

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.member = request.user
            team.save()
            return redirect('create_team')
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
            print(f"Error adding game: {e}")

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

    # Check if the user is the leader of the team
    if team.member == request.user:
        messages.error(request, "You cannot join a team you lead.")
        return redirect('home')

    # Check if the user is already a member of any team
    user_teams = TeamMember.objects.filter(user=request.user)
    if user_teams.exists():
        messages.error(request, "You are already a member of a team.")
        return redirect('home')

    # Create or get the join request
    join_request, created = JoinRequest.objects.get_or_create(team=team, user=request.user)
    print(join_request, created)  # Debug: Check if join request is created or exists

    if created:
        messages.success(request, "Join request sent successfully.")
    else:
        messages.info(request, "You have already requested to join this team.")

    return redirect('home')

@login_required
def join_requests(request):
    join_requests = JoinRequest.objects.filter(status='pending')  # Adjust the filter based on your requirements
    print(join_requests)  # For debugging
    return render(request, 'join_request.html', {'join_requests': join_requests})

def accept_join_request(request, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id)
    team = join_request.team
    user = join_request.user

    # Check if the user is already a member of this team
    if TeamMember.objects.filter(team=team, user=user).exists():
        messages.error(request, 'You are already a member of this team.')
        return redirect('join_requests')
    
    # Check if the join request is already approved or rejected
    if join_request.status in ['approved', 'rejected']:
        messages.error(request, 'This join request has already been processed.')
        return redirect('join_requests')

    # Approve the join request
    join_request.status = 'approved'
    join_request.save()

    # Add the user to the team
    TeamMember.objects.create(team=team, user=user)

    # Optionally, delete the join request after processing
    join_request.delete()

    messages.success(request, 'Join request approved successfully.')
    return redirect('join_requests')
    
    # Optionally, delete the join request after approval
    join_request.delete()
    
    messages.success(request, 'Join request approved successfully.')
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

    rank_choices = {
    'rov': {
        'Bronze': 1,
        'Silver': 2,
        'Gold': 3,
        'Platinum': 4,
        'Diamond': 5,
        'Commander': 6,
        'Conqueror': 7,
        'Supreme Conqueror': 8,
        'Glorious Ruler': 9
    },
    'valorant': {
        'Iron': 1,
        'Bronze': 2,
        'Silver': 3,
        'Gold': 4,
        'Platinum': 5,
        'Diamond': 6,
        'Ascendant': 7,
        'Immortal': 8,
        'Radiant': 9
    }
    }

    game_name = request.GET.get('gameName')
    rank_min = request.GET.get('rankMin')
    rank_max = request.GET.get('rankMax')

    selected_game = Game.objects.filter(id=game_name).first() if game_name else None

    if selected_game:
        teams = teams.filter(game=selected_game)

        game_key = selected_game.name.lower()
        if rank_min in rank_choices.get(game_key, []) and rank_max in rank_choices.get(game_key, []):
            teams = teams.filter(required_rank_min__lte=rank_min, required_rank_max__gte=rank_max)
    # Filter out teams that have enough members
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
        messages.error(request, "You cannot leave a team you lead.")
        return redirect('home')
    
    team_member = TeamMember.objects.filter(team=team, user=request.user).first()
    if team_member:
        team_member.delete()
        JoinRequest.objects.filter(team=team, user=request.user).delete()
        messages.success(request, "You have left the team.")
    else:
        messages.error(request, "You are not a member of this team.")
    
    return redirect('home')