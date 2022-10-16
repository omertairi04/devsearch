from django.shortcuts import render , redirect
from django.http import HttpResponse

from .models import Project
from .forms import ProjectForm
"""
projectsList = [

{'id': '1', 'title': 'Ecommerce Website', 'description': 'Fully functional ecommerce website' },

{ 'id': '2', 'title': 'Portfolio Website', 'description': 'A personal website to write articles and display work' },

{'id': '3', 'title': 'Social Network', 'description': 'An open source project built by the community' }

]

def test(____):
    queryset = ModelName.objects.all() or .get() | .filter() | .exclude()
"""

def projects(request):
    projects = Project.objects.all()
    context = {
        'projects':projects,
        }
    return render(request, "projects/projects.html", context)
#   return render(request, "projects/projects.html", {'____':msg}) ~ Qysh thirret ntemplates

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    context = {
        'project':projectObj,
        #'tags':tags,
        }
    return render(request, "projects/single-project.html" , context)

def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {
        'form':form,
    }
    return render(request , 'projects/project_form.html', context)

def updateProject(request , pk):
    project = Project.objects.get(id=pk) # merr id e postimit qe dojm me bo update
    form = ProjectForm(instance=project) # i mush fields me tdhanat qe jan
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {
        'form':form,
    }
    return render(request , 'projects/project_form.html', context)

def deleteProject(request , pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {
        'object':project,
    }
    return render(request , 'projects/delete_template.html', context)

