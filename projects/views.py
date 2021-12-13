from django.shortcuts import redirect, render
from .forms import ProjectForm
from projects.models import Project

# Create your views here.


def project(request, id):
    queryset = Project.objects.get(pk=id)
    context = {
        'project': queryset,
    }
    return render(request, 'projects/single-project.html', context)


def projects(request):
    queryset = Project.objects.all().order_by('-created')

    context = {
        'projects': queryset,
    }
    return render(request, 'projects/projects.html', context)


def createProject(request):

    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')

    content = {'form': form}
    return render(request, 'projects/new-project.html', content)


def updateProject(request, id):
    queryset = Project.objects.get(pk=id)
    form = ProjectForm(instance = queryset)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=queryset)
        if form.is_valid():
            form.save()

        return redirect('projects')
        

    content = {'form' : form}
    return render(request, 'projects/update.html', content)


def deleteProject(request, id):
    queryset = Project.objects.get(pk=id)
    if queryset:
            queryset.delete()
    return redirect('projects')

