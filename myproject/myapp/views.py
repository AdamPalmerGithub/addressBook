from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import ABUser, Contact, Tag, generate_random_color
from django.contrib.auth import authenticate, login as auth_in, logout as auth_out
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from datetime import datetime
import requests
from .forms import ContactForm, ContactUpdateForm, UserUpdateForm, LoginForm, SignUpForm


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
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            auth_user = authenticate(request, username=login_form.cleaned_data.get('username'), password=login_form.cleaned_data.get('password'))
            if auth_user is not None:
                auth_in(request, auth_user)
                return redirect("addressBook")
            else:
                login_form = LoginForm()
                return render(request, "login.html", {"error": "Invalid Credentials", "loginForm": login_form})
        else:
            login_form = LoginForm()
            return render(request, "login.html", {"error": "Invalid Credentials", "loginForm": login_form})
    else:
        login_form = LoginForm()
        return render(request, "login.html", {"loginForm":login_form})


def signup(request):
    if request.method == "POST":
        user_group = Group.objects.get(name='user')
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = ABUser.objects.create_user(
                username=form.cleaned_data.get('username'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                password=form.cleaned_data.get('password'),
                phone_number=form.cleaned_data.get('phone_number'),
                email=form.cleaned_data.get('email'),
            )
            new_user.groups.add(user_group)

            return redirect("login")
        else:
            sign_up = SignUpForm()
            return render(request, "signup.html", {"signUpForm": sign_up})
    else:
        form = SignUpForm()
        return render(request, "signup.html", {"signUpForm": form})


def logout(request):
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


@permission_required('myapp.add_contact', login_url="login")
@permission_required('myapp.view_contact', login_url="login")
@login_required(login_url="login")
def addContact(request):
    if request.method == "POST":
        add_form = ContactForm(request.POST)
        if add_form.is_valid():
            first_name = add_form.cleaned_data.get('first_name')
            last_name = add_form.cleaned_data.get('last_name')
            email_address = add_form.cleaned_data.get('email_address', None)
            phone_number = add_form.cleaned_data.get('phone_number', None)
            postcode = add_form.cleaned_data.get('postcode', None)
            tag_names = add_form.cleaned_data.get('tags', '')
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
    else:
        form = ContactForm()
        return render(request, "addContact.html", {"addForm": form})


@permission_required('myapp.change_contact', login_url="login")
@login_required(login_url="login")
def updateContact(request, id):
    if request.method == "POST":
        contact = get_object_or_404(Contact, id=id)

        updated_form = ContactUpdateForm(request.POST)

        if updated_form.is_valid():
            contact.first_name = updated_form.cleaned_data["first_name"]
            contact.last_name = updated_form.cleaned_data["last_name"]
            contact.email_address = updated_form.cleaned_data["email_address"]
            contact.phone_number = updated_form.cleaned_data["phone_number"]
            contact.postcode = updated_form.cleaned_data["postcode"]
            contact.save()

            tag_names = updated_form.cleaned_data.get('tags', '')  # Get tags as comma-separated string
            tag_names = [t.strip() for t in tag_names.split(',') if t.strip()]  # Clean list

            contact.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
                contact.tags.add(tag)

            return redirect("addressBook")
    else:
        contact = get_object_or_404(Contact, id=id)
        update_form = ContactUpdateForm()
        update_form.fields['first_name'].initial = contact.first_name
        update_form.fields['last_name'].initial = contact.last_name
        update_form.fields['phone_number'].initial = contact.phone_number
        update_form.fields['email_address'].initial = contact.email_address
        update_form.fields['postcode'].initial = contact.postcode

        all_tags = contact.tags.all()

        tag_values = [tag.name for tag in all_tags]
        tags = ""
        for i in range(len(tag_values)):
            tags += f"{tag_values[i]}, "
        update_form.fields['tags'].initial = tags

        return render(request, "updateContact.html", {"contact": contact,"updateForm": update_form})


@permission_required('myapp.delete_contact', login_url="login")
@login_required(login_url="login")
def deleteContact(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    return redirect('addressBook')


@permission_required(perm='myapp.change_abuser', login_url="login")
@login_required(login_url="login")
def settings(request):
    if request.method == "POST":
        user=ABUser.objects.get(id=request.user.id)

        updated_form = UserUpdateForm(request.POST)

        if updated_form.is_valid():
            user.username = updated_form.cleaned_data['username']
            user.first_name = updated_form.cleaned_data['first_name']
            user.last_name = updated_form.cleaned_data['last_name']
            user.phone_number = updated_form.cleaned_data['phone_number']
            user.email = updated_form.cleaned_data['email_address']

            password = updated_form.cleaned_data.get('password')
            if len(password) > 1:
                user.set_password(password)

            user.save()
            return redirect("login")
    else:
        user = ABUser.objects.get(id=request.user.id)
        update_form = UserUpdateForm()
        update_form.fields['username'].initial = user.username
        update_form.fields['first_name'].initial = user.first_name
        update_form.fields['last_name'].initial = user.last_name
        update_form.fields['phone_number'].initial = user.phone_number
        update_form.fields['email_address'].initial = user.email
        # TODO: delete form
        return render(request,"settings.html", {"updateForm": update_form})


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