from django.shortcuts import render
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm, loginForm
from .models import userInformation


# Create your views here.
def home(request):
    return render(request, 'home.html', )


def signup_view(request):

    if request.method == 'POST':

        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'], email = request.POST['email'])
                user.save()

                profile = userInformation(user = user, birthdate = request.POST['birthdate'], preferences = request.POST['preferences'], profile_picture = request.POST['profile_picture'], points = 0)
                profile.save()

                login(request, user)
                return redirect('home')
            
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreateForm, 'error':'Username already taken. Choose new username.'})

        else: return render(request, 'signup.html', {'form': UserCreateForm, 'error':'Passwords do not match'})
    
    return render(request, 'signup.html', {'form': UserCreateForm})


def profile(request):

    user_info = userInformation.objects.get(user=request.user)
    return render(request, 'profile.html', {'userInfo':user_info})



def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': loginForm()})
    else:
        form = loginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'login.html', {'form': form})


@login_required       
def logout_view(request):
    logout(request)
    return redirect('home')