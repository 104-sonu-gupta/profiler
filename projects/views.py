from django.shortcuts import redirect, render, HttpResponseRedirect
from .forms import ProjectForm, ReviewForm
from projects.models import Project, Review
from tags.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .utils import SearchProject
from django.db import IntegrityError
from django.core.paginator import Paginator


def project(request, id):
    curr_project = Project.objects.get(pk=id)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            review = form.save(commit=False)

            # Check that current user cannot vote his own project
            if request.user.profile == curr_project.owner:
                print(request.user, curr_project.owner)
                messages.error(request, 'You cannot vote your own project !!')
            
            else:
                try:
                    review.owner = request.user.profile
                    review.project = Project.objects.get(pk=id)
                    review.save()
                    messages.success(request, ("Review added !"))
                    # Update vote count, we can simply call the updateVote function which is set as property
                    curr_project.updateVote

                except IntegrityError:
                    messages.info(request, 'You have already voted')
            
            return HttpResponseRedirect('/projects/project/%s'%id)
        else:
            messages.error(request, ("You must be logged in to comment !"))
            return redirect('login')
            



    reviews = Review.objects.filter(project__id = id)
    context = {
        'project': curr_project,
        'reviews': reviews,
        'form' : form, 
    }
    return render(request, 'projects/single-project.html', context)


def projects(request):
    projects, search_query = SearchProject(request)
    
    paginator = Paginator(projects, 6)
    page = request.GET.get('page')
    
    projects = paginator.get_page(page)

    context = {
        'projects': projects,
        'search_query' : search_query,
    }
    return render(request, 'projects/projects.html', context)


@login_required(login_url='login')
def createProject(request):
    developer = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        tagsReceived = (request.POST['newtags']).replace(',', " ").split()
        # print(tagsReceived)
        newtags = list()
        for tag in tagsReceived:
            tag = tag.strip('[{""}]')
            tag = tag[8:]
            print(tag)
            newtags.append(tag)
            
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project_instance = form.save(commit=False)
            project_instance.owner = developer

            project_instance = form.save()
            for tag in newtags:
                tag = tag.upper()
                curr_tag, created = Tag.objects.get_or_create(name = tag)
                project_instance.tags.add(curr_tag)


            project_instance.save()
            messages.success(request, ("Project added successfully !"))
            return redirect('account')
        else:
            messages.error(
                request, ("Something went wrong, project was not added !"))

    content = {'form': form}
    return render(request, 'projects/new-project.html', content)


@login_required(login_url='login')
def updateProject(request, id):
    profile = request.user.profile
    project = None
    try:
        project = profile.project_set.get(pk=id)

    except ObjectDoesNotExist:
        messages.error(request, "You are not authorised to edit this project")
        return redirect('account')

    form = ProjectForm(instance=project)
    if request.method == "POST":
        # (use regex or replace for unknown input) 
        tagsReceived = (request.POST['newtags']).replace(',', " ").split()
        # print(tagsReceived)
        newtags = list()
        for tag in tagsReceived:
            tag = tag.strip('[{""}]')
            tag = tag[8:]
            print(tag)
            newtags.append(tag)

        # clear all the associated tags in project and then again assign them
        # so that we dont need to use API for this
        project.tags.clear()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()

            for tag in newtags:
                tag = tag.upper()   # capitalize all tags 
                curr_tag, created = Tag.objects.get_or_create(name = tag)

                project.tags.add(curr_tag)
            messages.success(request, "Project updated !")
        return redirect('account')

    content = {
        'form': form,
        'project': project,
    }
    return render(request, 'projects/update.html', content)


@login_required(login_url='login')
def deleteProject(request, id):

    # method 2 to check for correct user able to update project
    try:
        project = Project.objects.get(pk=id)
    except:
        messages.error(request, ("Project doesn't exists !"))
        return redirect('account')

        
    if request.user.profile == project.owner:
        context = {
            'type' : 'project',
            'name' : project.title,
        }
        if request.method=='POST':
            project.delete()
            messages.info(request, ("Project deleted !"))
        return render(request, 'confirm_delete.html', context)

    else:
        messages.error(request, ("You are not authorised to delete this project !"))
        return redirect('account')
