from django.shortcuts import render, redirect, get_object_or_404
from .models import ABUser, Contact
from django.contrib.auth import authenticate, login as auth_in, logout as auth_out
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q



# Create your views here.
def landing(request):
    return render(request, "index.html", {})


def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "signup.html", {})


def adduser(request):
    user_group = Group.objects.get(name='user')
    new_user = ABUser.objects.create_user(
        username=request.POST['user'],
        first_name=request.POST['first'],
        last_name=request.POST['last'],
        password=request.POST['pwd'],
        phone_number=request.POST['contact'],
        email=request.POST['email'],
    )
    new_user.groups.add(user_group)

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


@permission_required('myapp.view_contact', raise_exception=True)
@login_required(login_url="login")
def addressBook(request):
    user = request.user
    sort_by = request.GET.get("sort", "first_name")
    order_by = request.GET.get("order", "asc")
    search_query = request.GET.get("search", "").strip()

    sorted_field = f"-{sort_by}" if order_by == "desc" else sort_by

    mycontacts = Contact.objects.filter(addr_bk_id_id=user)
    
    if search_query:
        mycontacts = mycontacts.filter(
            Q(first_name__icontains=search_query) |  
            Q(last_name__icontains=search_query) |  
            Q(email_address__icontains=search_query)
    )

    mycontacts = mycontacts.order_by(sorted_field)

    return render(request, "addressBook.html", {
    "user": user,
    "mycontacts": mycontacts,
    "sort_by": sort_by,
    "order_by": order_by,
    "search_query": search_query
})


@permission_required('myapp.add_contact', raise_exception=True)
@login_required(login_url="login")
def addContact(request):
    return render(request, "addContact.html", {})


@permission_required('myapp.add_contact', raise_exception=True)
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




@permission_required('myapp.change_contact', raise_exception=True)
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

@permission_required('myapp.delete_contact', raise_exception=True)
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

@permission_required(perm='myapp.change_abuser', raise_exception=True)
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

@permission_required(perm='myapp.delete_abuser', raise_exception=True)
@login_required(login_url="login")
def delete(request):
    del_user=ABUser.objects.get(id=request.user.id)
    del_user.delete()
    return redirect("login")