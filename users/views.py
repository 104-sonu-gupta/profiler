from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from projects.models import Project
from .utils import SearchDeveloper

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, ('Username does not exists'))
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('Logged In Successfully! '))
            return redirect('account')
        else:
            messages.error(request, ('Username or passsword is incorrect'))

    context = {
        'page': 'login',
    }
    return render(request, 'login_register.html', context)


def logoutPage(request):
    logout(request)
    messages.info(request, ('Logged Out Successfully! '))
    return redirect('login')


def registerUser(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, (" User account created !"))
            login(request, user)    # created and login this user directly
            return redirect('edit-account')
        else:
            messages.error(
                request, (" An error has been occcurred, try to register again !"))

    context = {
        'page': 'register',
        'form': form
    }
    return render(request, 'login_register.html', context)


def profiles(request):
    profiles, search_query = SearchDeveloper(request)
    context = {
        'profiles': profiles,
        'search_query' : search_query
    }
    return render(request, 'profiles.html', context)


def individualprofile(request, id):
    profile = userProfile.objects.get(pk=id)

    topSkills = profile.skill_set.exclude(description__exact='')
    otherSkills = profile.skill_set.filter(description='')
    projects = Project.objects.filter(owner=profile).order_by('-created')     
    # extract and order by latest project of user
    # OR we could use {% for project in profile.project_set.all %}  in HTML Template

    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills,
        'projects': projects,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    context = {
        'profile': profile,
        'skills': skills,
    }
    return render(request, 'account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = userProfileForm(instance = profile)
    if request.method == "POST":
        form = userProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        'form': form,
    }
    return render(request, 'profile_form.html', context)

@login_required(login_url='login')
def addSkill(request):
    
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill_instance = form.save(commit=False)
            skill_instance.owner = profile
            skill_instance.save()

            messages.success(request, ("Skill added successfully !"))
            return redirect('account')
        else:
            messages.error(request, ("Something went wrong, try again !"))

    context = {
        'form' : form,
        'work' : 'add',
    }
    return render(request, 'skill_form.html', context)


@login_required(login_url='login')
def editSkill(request, id):
    profile = request.user.profile
    skill = None
    try:
        skill = profile.skill_set.get(pk=id)
    except ObjectDoesNotExist:
        messages.error(request, "You are not authorised to edit this skill")
        return redirect('account')

    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "skill updated !")
        return redirect('account')
    content = {
        'form': form,
        'work' : 'update',
    }
    return render(request, 'skill_form.html', content)


def deleteSkill(request, id):
    profile = request.user.profile
    skill = None
    try:
        skill = profile.skill_set.get(pk=id)
    except ObjectDoesNotExist:
        messages.error(request, "You are not authorised to delete this skill")
        return redirect('account')

    if request.method == 'POST':
        messages.info(request, ("Skill deleted !"))
        skill.delete()
        
    return redirect('account')