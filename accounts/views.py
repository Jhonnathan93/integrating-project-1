from django.shortcuts import render
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm, loginForm
from .models import UserProfile


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup_view(request):

    if request.method == 'POST':

        if request.POST['password1'] == request.POST['password2']:

            user = User.objects.create_user(request.POST['username'], password = request.POST['password1'], email = request.POST['email'])
            user.save()
            print(user)

            profile = UserProfile(user = user, birthdate = request.POST['birthdate'], preferences = request.POST['preferences'], profile_picture = request.POST['profile_picture'])
            profile.save()
            print(profile)

            return render(request, 'home.html') 

            login(request, user)
            return redirect('home')

    return render(request, 'signup.html', {'form': UserCreateForm})


# def signup_view(request):
    
#     if request.method == 'GET':
#         return render(request, 'signup.html',
#             {'form':UserCreateForm})
#     else:
#         if request.POST['password1'] == request.POST['password2']:
        
#             form = UserCreateForm(request.POST)

#             if form.is_valid():
#                 try:
#                     user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
#                     user.save()
#                     login(request, user)
#                     return redirect('home')
#                 except IntegrityError:
#                     return render(request, 'signup.html',
#                     {'form':UserCreateForm,
#                     'error':'El nombre de usuario ya está en uso.'})
#             else:
#                 return render(request, 'signup.html', {'form': form})
#         else:
#             return render(request, 'signup.html',
#             {'form':UserCreateForm, 'error':'Contraseñas no coinciden'})


# def login_view(request):
#     if request.method == 'GET':
#         return render(request, 'login.html',{'form':AuthenticationForm})
#     else:
#         user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
#     if user is None:
#         return render(request,'login.html',{'form': AuthenticationForm(),'error': 'Usuario y contraseña no coinciden'})
#     else:
#         login(request,user)
#     return redirect('home')



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