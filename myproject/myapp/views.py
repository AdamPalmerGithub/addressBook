from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request,"index.html",{})

def login(request):
    return render(request, "login.html",{})

@login_required
def app(request):
    pass