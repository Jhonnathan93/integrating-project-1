from django.shortcuts import render
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup_view(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html',
            {'form':UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
        
            form = UserCreateForm(request.POST)

            if form.is_valid():
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('home')
                except IntegrityError:
                    return render(request, 'signup.html',
                    {'form':UserCreateForm,
                    'error':'Username already taken. Choose new username.'})
            else:
                return render(request, 'signup.html', {'form': form})
        else:
            return render(request, 'signup.html',
            {'form':UserCreateForm, 'error':'Passwords do not match'})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html',{'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
    if user is None:
        return render(request,'login.html',{'form': AuthenticationForm(),'error': 'username and password do not match'})
    else:
        login(request,user)
    return redirect('home')


@login_required       
def logout_view(request):
    logout(request)
    return redirect('home')