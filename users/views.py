from django.shortcuts import render , redirect
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q 

from .models import Profile , Message
from .forms import CustomUserCreationForm , ProfileForm , SkillForm , MessageForm
from .utils import searchProfiles ,paginateProfiles

def profiles(request):
    # i mormi prej serachProfiles - kur i bojm return 
    profiles , search_query = searchProfiles(request)
    custom_range , profiles = paginateProfiles(request,profiles,15)

    context = {
        'profiles':profiles,
        'search_query':search_query,
        'custom_range':custom_range,
    }
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {
        'profile':profile,
        'topSkills':topSkills,
        'otherSkills':otherSkills
    }
    return render(request , 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    # get logged in user - per me query one to one 
    profile = request.user.profile
    # get user skill - modelName_set - per me i query many to many 
    skills = profile.skill_set.all()
    # get user projects - modelName_set - per me i query one to many
    projects = profile.project_set.all()
    context = {
        'profile':profile,
        'skills':skills,
        'projects':projects
    }
    return render(request , 'users/account.html',context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST , request.FILES , instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        'form':form
    }
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill was added successfully!')
            
            return redirect('account')

    context = {
        'form':form,
    }
    return render(request , 'users/skill_form.html' ,context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance = skill)
    if request.method == 'POST':
        form = SkillForm(request.POST , instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill was updated successfully!')
            return redirect('account')

    context = {
        'form':form,
    }
    return render(request , 'users/skill_form.html' ,context)

@login_required(login_url='login')
def deleteSkill(request , pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id = pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was successfully deleted!')
        return redirect('account')
    context = {
        'object':skill,
    }
    return render(request , 'delete_template.html',context)


def loginUser(request):
    page = 'login'
    # e kshyrmi se nqoftse a asht useri logged in, nqoftse po at'her e qojm te profiles , nqoftse jo vazhdojm
    if request.user.is_authenticated:
        return redirect('profiles')

    #  nqoftse metoda osht POST <HTML>
    if request.method == "POST":
        # i mormi emrin e inputeve nhtml dhe ja i lidhmi me variablat
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            # e kshyrmi se a osht usernemi ndatabaz
            user = User.objects.get(username=username)
        except:
            # nqoftse jo at'her e qojm ni message 
            """
            messages i regjistrojm tek main.html
            """
            messages.error(request , "Username does not exist")
        # nqoftese kejt jon nrregull at'her e bojm llog in 
        user = authenticate(request, username=username , password=password)
        # nqofte useri ndatabaz nuk osht i shprast , at'her e bojm llogin edhe e qojm tek profiles
        if user is not None:
            login(request , user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
        # nqoftse jo at'her e qesmi ket messazhin
            messages.error(request , "Username or password is incorrect")

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.success(request , "User was logged out!")
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            """
            Shpjegim i commit=False
            That's useful when you get most of your model data from a form, but you need to populate some null=False fields with non-form data.
            Saving with commit=False gets you a model object, then you can add your extra data and save it.
            This is a good example of that situation.
            Here's the documentation on the save method. Note that if your form includes many-to-many fields,
            you'll also want to call form.save_m2m() after saving the model instance.
            """
            user.username = user.username.lower()
            user.save()
            messages.success(request , "User created successfully!")

            login(request , user)
            return redirect('edit-account')
        else:
            messages.error(request, "An error has occurred during registration!")

    context = {
        'page':page,
        'form':form,
    }
    return render(request, 'users/login_register.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all() # messages - vlera e related_name
    unreadCount = messageRequests.filter(is_read=False).count()

    context = {
        'messageRequests':messageRequests,
        'unreadCount':unreadCount
    }
    return render(request , 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request , pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)  # messages - vlera e related_name
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request , 'users/message.html',context)

def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            # add sender to message
            message.sender = sender
            # add recipient to message
            message.recipient = recipient

            if sender:
                # when user is signedd in we send the name and email manually through this
                message.name = sender.name
                message.email = sender.email
            
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('profile' , pk=recipient.id)

    context = {
        'recipient':recipient,
        'form':form
    }   
    return render(request , 'users/message_form.html',context)