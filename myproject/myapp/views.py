from django.shortcuts import render, redirect, get_object_or_404
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


def logoutuser(request):
    auth_out(request)
    return redirect("landing")


@login_required(login_url="login")
def addressBook(request):
    user = request.user
    sort_by = request.GET.get("sort", "first_name")
    order_by = request.GET.get("order", "asc")

    if order_by == "desc":
        sort_by = f"-{sort_by}"
    mycontacts = Contact.objects.filter(addr_bk_id_id=user).order_by(sort_by)
    return render(request, 'addressBook.html', {'user': user, 'mycontacts': mycontacts, "sort_by": sort_by})

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

@login_required(login_url="login")
def updateContact(request, id):
    contact = get_object_or_404(Contact, id=id)
    return render(request, "updateContact.html", {"contact": contact})

@login_required(login_url="login")
def updateContactSubmit(request, id=id):
    contact = get_object_or_404(Contact, id=id)

    if request.method == "POST":
        contact.first_name = request.POST["first_name"]
        contact.last_name = request.POST["last_name"]
        contact.email_address = request.POST["email_address"]
        contact.phone_number = request.POST["phone_number"]
        contact.postcode = request.POST["postcode"]
        contact.save()

        return redirect("addressBook")
    return render(request, "updateContact.html", {"contact": contact})

@login_required(login_url="login")
def deleteContact(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    return redirect('addressBook')

@login_required(login_url="login")
def settings(request):
    return render(request, "settings.html")

@login_required(login_url="login")
def updateUser(request):
    user = request.user
    return render(request, "updateUser.html", {"user":user})

@login_required(login_url="login")
def update(request):
    if request.method == "POST":
        user=ABUser.objects.get(id=request.user.id)

        user.username = request.POST.get("user")
        user.first_name = request.POST.get("first")
        user.last_name = request.POST.get("last")
        user.phone_number = request.POST.get("contact")
        user.email = request.POST.get("email")

        password=request.POST.get("pwd")
        if len(password) > 1:
            user.set_password(password)

        user.save()
        return redirect("login")
    return render(request,"settings.html", {"user",request.user})

@login_required(login_url="login")
def delete(request):
    del_user=ABUser.objects.get(id=request.user.id)
    del_user.delete()
    return redirect("login")

