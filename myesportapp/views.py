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
                    return redirect('foradmin')  # แก้ไขเป็นชื่อ URL ที่เหมาะสมสำหรับหน้าผู้ดูแลระบบ
                else:
                    return redirect('home')  # แก้ไขเป็นชื่อ URL ที่เหมาะสมสำหรับหน้าผู้ใช้ทั่วไป
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

def my_team(req):
    return render(req,'my_team.html')


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

            return redirect('profile')  # Redirect to a profile page or success page
        else:
            print(profile_form.errors)
            print(formset.errors)
    else:
        profile_form = PlayerProfileForm()
        formset = WorkPictureFormSet(queryset=WorkPicture.objects.none())

    return render(request, 'profile.html', {'profile_form': profile_form, 'formset': formset})

def profile(request):
    # ใส่ logic สำหรับ view profile ของคุณที่นี่
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
    selected_game = None  # กำหนดค่าเริ่มต้นให้กับ selected_game

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_team')  # เปลี่ยนเป็น URL ที่คุณต้องการให้เปลี่ยนไป
    else:
        form = TeamForm()
        if 'game' in request.GET:
            try:
                game_id = int(request.GET['game'])
                selected_game = Game.objects.get(id=game_id)
                form.fields['required_rank_min'].choices = form.get_rank_choices(selected_game)
                form.fields['required_rank_max'].choices = form.get_rank_choices(selected_game)
                form.initial['game'] = selected_game  # ตั้งค่า initial value ของฟิลด์เกม
            except (ValueError, TypeError, Game.DoesNotExist):
                selected_game = None  # ตั้งค่าเป็น None เมื่อไม่สามารถหาเกมได้

    return render(request, 'create_team.html', {'form': form, 'selected_game': selected_game})

@login_required
def create_game(req):
    return render(req,'create_game_admin.html')


def my_team(request):
    has_profile = PlayerProfile.objects.filter(member=request.user).exists()
    if has_profile:
        teams = Team.objects.filter(member=request.user)
    else:
        teams = []
    return render(request, 'my_team.html', {'teams': teams, 'has_profile': has_profile})

def team_list(request):
    teams = Team.objects.all()  # ดึงข้อมูลทีมทั้งหมด
    return render(request, 'home.html', {'teams': teams})

def foradmin(req):
    return render(req,'foradmin.html')

def add_game(request):
    if request.method == 'POST':
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

        # สร้างอ็อบเจ็กต์ Game และบันทึกข้อมูลลงในฐานข้อมูล
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

        # รีไดเร็กไปยังหน้าความสำเร็จ (หรือหน้าอื่นๆ ที่คุณต้องการ)
        return redirect('success_page')  # คุณต้องสร้างหน้า success_page เอง

    # ถ้าเป็นคำขอ GET ให้แสดงฟอร์ม
    return render(request, 'add_game.html')

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
    join_request, created = JoinRequest.objects.get_or_create(team=team, user=request.user)
    return redirect('home')

@login_required
def manage_join_requests(request):
    if request.user.is_superuser:
        join_requests = JoinRequest.objects.all()
    else:
        join_requests = JoinRequest.objects.filter(team__member=request.user)
    return render(request, 'manage_requests.html', {'join_requests': join_requests})

@login_required
def handle_request(request, request_id, action):
    join_request = get_object_or_404(JoinRequest, id=request_id)
    if action == 'approve':
        join_request.approved = True
        join_request.rejected = False
    elif action == 'reject':
        join_request.approved = False
        join_request.rejected = True
    join_request.save()
    return redirect('manage_requests')
