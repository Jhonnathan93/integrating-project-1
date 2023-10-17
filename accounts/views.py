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
from readinglists.models import ReadingList



# Create your views here.
def home(request):
    return render(request, 'home.html', )


def signup_view(request):
    
    if request.method == 'POST':

        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'], email = request.POST['email'])
                user.save()

                profile_picture = request.FILES.get('profile_picture')
                
                profile = userInformation(user = user, birthdate = request.POST['birthdate'], preferences = request.POST['preferences'], profile_picture = profile_picture, points = 0)
                profile.save()

                login(request, user)
                return redirect('home')
            
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreateForm, 'error':'Username already taken. Choose new username.'})

        else: return render(request, 'signup.html', {'form': UserCreateForm, 'error':'Passwords do not match'})
    
    return render(request, 'signup.html', {'form': UserCreateForm})

@login_required
def profile(request):
    # Obtiene la instancia de userInformation para el usuario actual.
    user_info = userInformation.objects.get(user=request.user)
    
    # Accede a los atributos del objeto userInformation.
    birthdate = user_info.birthdate
    preferences = user_info.preferences
    profile_picture = user_info.profile_picture
    points = user_info.points
    readinglists = ReadingList.objects.filter(user=request.user).order_by('-date_created')

    # Luego, puedes pasar estos datos a tu plantilla.
    return render(request, 'profile.html', {
        'birthdate': birthdate,
        'preferences': preferences,
        'profile_picture': profile_picture,
        'points': points,
        'readinglists': readinglists,
    })


def editprofile(request):
    user_info = userInformation.objects.get(user=request.user)
    
    if request.method == 'GET':
        
        form= UserCreateForm(instance=user_info)
        return render(request, 'editprofile.html', {'form': form})
    else:
        try:
            form = UserCreateForm(request.POST, request.FILES, instance=user_info)
            form.save()
            
            return redirect('profile', user_info)
        except ValueError:
            return render(request, 'editprofile.html',{'user_info': user_info,'form':form,'error':'Bad data in form'})
        

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