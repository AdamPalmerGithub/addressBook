from django.contrib.auth.decorators import login_required
from django.db.models.functions import datetime
from django.shortcuts import render, redirect
from .models import ABUser,Contact


# Create your views here.
def landing(request):
    return render(request, "index.html", {})


def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "signup.html", {})

def addressBook(request):
    user = request.user
    mycontacts = Contact.objects.filter(addr_bk_id_id=user)  
    return render(request, 'addressBook.html', {'user': user, 'mycontacts': mycontacts})

def addContact(request):
    return render(request, "addContact.html", {})

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
