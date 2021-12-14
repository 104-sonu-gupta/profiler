from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import CustomRegistrationForm

from django.contrib import messages

from projects.models import Project
from .models import userProfile
# Create your views here.


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('profiles')

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
            return redirect('profiles')
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
            return redirect('profiles')
        else:
            messages.error(
                request, (" An error has been occcurred, try to register again !"))

    context = {
        'page': 'register',
        'form': form
    }
    return render(request, 'login_register.html', context)


def profiles(request):
    queryset = userProfile.objects.all()
    # skill = Skill.objects.get
    context = {
        'profiles': queryset
    }

    return render(request, 'profiles.html', context)


def individualprofile(request, id):
    profile = userProfile.objects.get(pk=id)

    topSkills = profile.skill_set.exclude(description__exact='')
    otherSkills = profile.skill_set.filter(description='')
    projects = Project.objects.filter(owner=profile).order_by('-created')     # extract and order by latest project of user
    # OR we could use {% for project in profile.project_set.all %}  in HTML Template

    context = {

        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills,
        'projects': projects,

    }

    return render(request, 'profile.html', context)
