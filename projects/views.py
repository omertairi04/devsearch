from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator ,PageNotAnInteger , EmptyPage
from django.contrib import messages

from .models import Project , Tag
from .forms import ProjectForm , ReviewForm
from .utils import searchProjects , paginateProjects
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
    projects , search_query = searchProjects(request)

    custom_range , projects = paginateProjects(request , projects , 12)

    context = {
        'projects':projects,
        'search_query':search_query,
#       'paginator':paginator,
        'custom_range':custom_range
        }
    return render(request, "projects/projects.html", context)
#   return render(request, "projects/projects.html", {'____':msg}) ~ Qysh thirret ntemplates

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    #tags = projectObj.tags.all()
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        # sets review.modelField[project] to the project which this form is
        review.project = projectObj
        # sets review.modelField[owner] to the request.user.profile 
        review.owner = request.user.profile
        review.save()
        # update project vote count!
        projectObj.getVoteCount

        messages.success(request,"Your review has been submitted")
        # sends the user to 'project' and the projectOBJ id
        return redirect('project' ,pk=projectObj.id)

    context = {
        'project':projectObj,
        #'tags':tags,
        'form':form,
        }
    return render(request, "projects/single-project.html" , context)

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST , request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('projects')
    context = {
        'form':form,
    }
    return render(request , 'projects/project_form.html', context)

@login_required(login_url="login")
def updateProject(request , pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk) # merr id e postimit qe dojm me bo update (many to many)
    form = ProjectForm(instance=project) # i mush fields me tdhanat qe jan
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'form':form,
    }
    return render(request , 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request , pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {
        'object':project,
    }
    return render(request , 'delete_template.html', context)

