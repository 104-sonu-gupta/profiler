from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import *
from .models import *
from .utils import *
from projects.models import Project


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('account')

    username = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, ('Username does not exists'))
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, ('Logged In Successfully! '))
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, ('Incorrect Passsword !'))

    context = {
        'page': 'login',
        'username' : username, 
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

    context = {
        'page': 'register',
        'form': form
    }
    return render(request, 'login_register.html', context)


def profiles(request):
    profiles, search_query = SearchDeveloper(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)
    
    context = {
        'profiles': profiles, 
        'search_query': search_query,
        'custom_range': custom_range,
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
            messages.success(request, ("Profile updated !"))
            return redirect('account')
        else:
            messages.error(request, ("Something went wrong, try again !"))

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
        if form.is_valid() :
            skill_instance = form.save(commit=False)
            skill_instance.owner = profile
            if skill_instance.name:
                skill_instance.save()
                messages.success(request, ("Skill added successfully !"))
            else:
                messages.error(request, ("Empty skill not allowed !"))



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

@login_required(login_url='login')
def deleteSkill(request, id):
    profile = request.user.profile
    try:
        skill = profile.skill_set.get(pk=id)
       
    except ObjectDoesNotExist:
        messages.error(request, "You are not authorised to delete this skill")
        return redirect('account')

    if request.method == 'POST':
        messages.info(request, (" Skill deleted !"))
        skill.delete()
        return redirect('account')

    content = {
        'type': 'skill',
        'name' : skill.name
    }
    return render(request, 'confirm_delete.html', content)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    inbox = profile.messages.all()
    unread_count = inbox.filter(is_read=False).count()
    
    content={
        'inbox' : inbox, 
        'unread_count': unread_count,
    }
    return render(request, 'inbox.html', content)

@login_required(login_url='login')
def viewMessage(request, id):
    profile = request.user.profile
    userMessage = profile.messages.get(pk=id)
    userMessage.is_read = True
    userMessage.read_at = timezone.now()
    userMessage.save()
    
    try:
        sender_id = userMessage.sender.id
    except:
        sender_id = ''
    
    content = {
        'message' : userMessage,
        'sender_id' : sender_id,
    }
    return render(request, 'message.html', content)


def sendMessage(request, pk):
    recipient = userProfile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.reciever = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', id=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'message_form.html', context)