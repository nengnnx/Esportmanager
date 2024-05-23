# myesportapp/views.py
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
                return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def profile(req):
    return render(req,'prifile.html')

def search(req):
    return render(req,'search.html')

@login_required
def finding(req):
    return render(req,'finding.html')

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
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user
            team.save()
            messages.success(request, 'ทีมของคุณถูกสร้างเรียบร้อยแล้ว!')
            return redirect('team_list')  # เปลี่ยน 'team_list' เป็นชื่อ URL ที่คุณต้องการเปลี่ยนไป
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form})

