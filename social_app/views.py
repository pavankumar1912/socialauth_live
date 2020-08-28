from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import CreateUserForm

# Create your views here.

@login_required(login_url= 'login')
def home(request):
    return render(request, 'social_app/index.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            userexits = User.objects.filter(username = username)
            if userexits.exists():
                messages.info(request, f'password is incorrect for entered user {username}')
            else:
                messages.info(request, f'{username} user is not exists')
    context = {}
    return render(request, 'social_app/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'social_app/register.html', context)