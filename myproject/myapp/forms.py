from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True, label="First Name")
    last_name = forms.CharField(max_length=100, required=True, label="Last Name")
    email_address = forms.EmailField(required=False, label="Email")
    phone_number = forms.CharField(max_length=15, required=False, label="Phone Number")
    postcode = forms.CharField(max_length=20, required=False, label="Postcode")
    tags = forms.CharField(widget=forms.TextInput(), required=False, label="Tags (comma-separated)")

class UserUpdateForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, label="Username")
    first_name = forms.CharField(max_length=100, required=True, label="First Name")
    last_name = forms.CharField(max_length=100, required=True, label="Last Name")
    email_address = forms.EmailField(required=True, label="Email")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    password = forms.CharField(
        max_length=50,
        required=False,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                'class': 'form-inputs',
            }
        )
    )

class ContactUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True, label="First Name")
    last_name = forms.CharField(max_length=100, required=True, label="Last Name")
    email_address = forms.EmailField(required=False, label="Email")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    postcode = forms.CharField(max_length=20, required=False, label="Postcode")
    tags = forms.CharField(widget=forms.TextInput(), required=False, label="Tags (comma-separated)")

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        label="Username",
        widget = forms.TextInput(
            attrs={
                'placeholder': 'Enter your username',
                'class': 'form-inputs',
            }
        )
    )
    password = forms.CharField(
        max_length=50,
        required=True,
        label="Password",
        widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                'class': 'form-inputs',
            }
        )
    )


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, label="Username")
    first_name = forms.CharField(max_length=100, required=True, label="First Name")
    last_name = forms.CharField(max_length=100, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput, label="Password")
    