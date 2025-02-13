from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import ABUser, Contact, Tag
from django.contrib.auth import authenticate, login as auth_in, logout as auth_out
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from datetime import datetime
import requests

# Create your views here.
def landing(request):
    url = 'https://api.open-meteo.com/v1/forecast?latitude=51.9022&longitude=-0.2026&current=temperature_2m,relative_humidity_2m&wind_speed_unit=mph&forecast_days=1'
    response = requests.get(url).json()
    current_data = response.get("current", {})
    date_time = current_data.get("time")
    dt = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
    date_today = dt.strftime("%d-%m-%Y")
    time = dt.strftime("%H:%M")
    temperature = current_data.get("temperature_2m")
    humidity = current_data.get("relative_humidity_2m")


    return render(request, "index.html", {
        "date": date_today,
        "time": time,
        "temperature": temperature,
        "humidity": humidity
    })


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

    return redirect("login")


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

  


@permission_required('myapp.view_contact', login_url="login")
@login_required(login_url="login")
def addressBook(request):
    user = request.user
    sort_by = request.GET.get("sort", "first_name")
    order_by = request.GET.get("order", "asc")
    search_query = request.GET.get("search", "").strip()
    selected_tags = request.GET.getlist("tags")

    sorted_field = f"-{sort_by}" if order_by == "desc" else sort_by

    mycontacts = Contact.objects.filter(addr_bk_id_id=user)
    
    if search_query:
        mycontacts = mycontacts.filter(
            Q(first_name__icontains=search_query) |  
            Q(last_name__icontains=search_query) |  
            Q(email_address__icontains=search_query)
    )
        
    if selected_tags and "" not in selected_tags:
        mycontacts = mycontacts.filter(tags__id__in=selected_tags).distinct()

    mycontacts = mycontacts.order_by(sorted_field)
    all_tags = Tag.objects.filter(user=user)

    return render(request, "addressBook.html", {
        "user": user,
        "mycontacts": mycontacts,
        "sort_by": sort_by,
        "order_by": order_by,
        "search_query": search_query,
        "all_tags": all_tags,
        "selected_tags": selected_tags
    })


@permission_required('myapp.view_contact', login_url="login")
@login_required(login_url="login")
def addContact(request):
    return render(request, "addContact.html", {})


@permission_required('myapp.add_contact', login_url="login")
@login_required(login_url="login")
def addContactsubmit(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('email_address', None)
        phone_number = request.POST.get('phone_number', None)
        postcode = request.POST.get('postcode', None)
        tag_names = request.POST.get('tags', '')
        # Create and save new contact
        contact = Contact.objects.create(
            addr_bk_id=request.user,
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            phone_number=phone_number,
            postcode=postcode
        )
        tag_names = [t.strip() for t in tag_names.split(',') if t.strip()]  # Clean list
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
            contact.tags.add(tag)

        return redirect('addressBook')
    return render(request, "addContact.html")


@login_required(login_url="login")
def updateContact(request, id):
    contact = get_object_or_404(Contact, id=id)
    return render(request, "updateContact.html", {"contact": contact})



@permission_required('myapp.change_contact', login_url="login")
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

        tag_names = request.POST.get('tags', '')  # Get tags as comma-separated string
        tag_names = [t.strip() for t in tag_names.split(',') if t.strip()]  # Clean list

        contact.tags.clear()
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
            contact.tags.add(tag)

        return redirect("addressBook")
    return render(request, "updateContact.html", {"contact": contact})

@permission_required('myapp.delete_contact', login_url="login")
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

@permission_required(perm='myapp.change_abuser', login_url="login")
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

@permission_required(perm='myapp.delete_abuser', login_url="login")
@login_required(login_url="login")
def delete(request):
    del_user=ABUser.objects.get(id=request.user.id)
    del_user.delete()
    return redirect("login")

@permission_required(perm="myapp.can_access_calendar", login_url="login")
@login_required(login_url="login")
def calendar(request, id):
    event_participant = Contact.objects.get(id=id)

    url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text=Event+with+{ event_participant.first_name }+{ event_participant.last_name }"

    html_content = f"""
            <html>
                <body>
                    <script type="text/javascript">
                        window.open("{url}", "_blank");
                        window.location.href = "/addressBook";
                    </script>
                </body>
            </html>
        """
    return HttpResponse(html_content)