from django.shortcuts import render, redirect
from .models import ABUser, Contact
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
        return redirect("addressBook")
    else:
        return render(request, "login.html", {"error": "Invalid Credentials"})

# addressBook.html

def logoutuser(request):
    auth_out(request)
    return redirect("landing")


@login_required(login_url="login")
def addressBook(request):
    return render(request, 'addressBook.html', {"user":request.user})

def addressBook(request):
    user = request.user
    mycontacts = Contact.objects.filter(addr_bk_id_id=user)
    return render(request, 'addressBook.html', {'user': user, 'mycontacts': mycontacts})

@login_required(login_url="login")
def addContact(request):
    return render(request, "addContact.html", {})

@login_required(login_url="login")
def addContactsubmit(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('email_address', None)
        phone_number = request.POST.get('phone_number', None)
        postcode = request.POST.get('postcode', None)
        # Create and save new contact
        Contact.objects.create(
            addr_bk_id=request.user,
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            phone_number=phone_number,
            postcode=postcode
        )
        return redirect('addressBook')
    return render(request, "addContact.html")