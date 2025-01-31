from django.contrib.auth.decorators import login_required
from django.db.models.functions import datetime
from django.shortcuts import render, redirect
from .models import ABUser


# Create your views here.
def landing(request):
    return render(request, "index.html", {})


def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "signup.html", {})


def adduser(request):
    new = ABUser(
        username=request.POST['user'],
        first_name=request.POST['first'],
        last_name=request.POST['last'],
        phone_number=request.POST['contact'],
        password=request.POST['pwd'],
        email=request.POST['email'],
        last_login=datetime.Now(),
    )

    new.save()

    #return redirect("app")
    return redirect("/")


@login_required
def app(request):
    pass
