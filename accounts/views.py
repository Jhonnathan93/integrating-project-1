from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from readinglists.selectors import reading_lists_for_user

from .selectors import user_profile_get
from .services import profile_update, user_register

SIGNUP_TEMPLATE = "signup.html"
BOOK_HOME_ROUTE = "book:home"


def signup_view(request):
    if request.method != "POST":
        return render(request, SIGNUP_TEMPLATE)
    if request.POST.get("password1") != request.POST.get("password2"):
        return render(
            request, SIGNUP_TEMPLATE, {"error": "Las contraseñas no coinciden."}
        )
    try:
        user = user_register(
            username=request.POST.get("username", "").strip(),
            email=request.POST.get("email", "").strip(),
            password=request.POST.get("password1", ""),
            birthdate=request.POST.get("birthdate"),
            preferences=request.POST.get("preferences", "").strip(),
            profile_picture=request.FILES.get("profile_picture"),
        )
    except IntegrityError, ValueError:
        return render(
            request,
            SIGNUP_TEMPLATE,
            {"error": "Revisa los datos o utiliza otro nombre de usuario."},
        )
    login(request, user)
    return redirect(BOOK_HOME_ROUTE)


@login_required
@require_GET
def profile(request):
    profile = user_profile_get(user=request.user)
    return render(
        request,
        "profile.html",
        {
            "birthdate": profile.birthdate,
            "preferences": profile.preferences,
            "profile_picture": profile.profile_picture,
            "points": profile.points,
            "readinglists": reading_lists_for_user(user=request.user),
        },
    )


@login_required
def editprofile(request):
    profile = user_profile_get(user=request.user)
    if request.method == "GET":
        return render(request, "editprofile.html", {"user_profile": profile})
    try:
        profile_update(
            profile=profile,
            username=request.POST.get("username", "").strip(),
            preferences=request.POST.get("preferences", "").strip(),
            profile_picture=request.FILES.get("profile_picture"),
        )
    except IntegrityError, ValueError:
        return render(
            request,
            "editprofile.html",
            {"user_profile": profile, "error": "No fue posible actualizar el perfil."},
        )
    return redirect("accounts:profile")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    user = authenticate(
        request,
        username=request.POST.get("usuario"),
        password=request.POST.get("contraseña"),
    )
    if user is None:
        return render(
            request, "login.html", {"error": "Usuario y contraseña no coinciden."}
        )
    login(request, user)
    return redirect(BOOK_HOME_ROUTE)


@login_required
@require_GET
def logout_view(request):
    logout(request)
    return redirect(BOOK_HOME_ROUTE)
