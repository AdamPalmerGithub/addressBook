from django.shortcuts import render, redirect
from .models import ABUser
from django.contrib.auth import authenticate, login as auth_in, logout as auth_out
from django.contrib.auth.decorators import login_required


# Create your views here.
def landing(request):
    return render(request, "index.html", {})


def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "signup.html", {})


def adduser(request):
    ABUser.objects.create_user(
        username=request.POST['user'],
        first_name=request.POST['first'],
        last_name=request.POST['last'],
        password=request.POST['pwd'],
        phone_number=request.POST['contact'],
        email=request.POST['email'],
    )

    return redirect("loginuser")


def loginuser(request):
    auth_user = authenticate(request, username=request.POST.get('user'), password=request.POST.get('pwd'))
    if auth_user is not None:
        auth_in(request, auth_user)
        return redirect("app")
    else:
        return render(request, "login.html", {"error": "Invalid Credentials"})

# addressBook.html

def logoutuser(request):
    auth_out(request)
    return redirect("landing")


@login_required(login_url="login")
def app(request):
    return render(request, 'addressBook.html', {"user":request.user})
