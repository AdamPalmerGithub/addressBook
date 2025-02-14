from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="First Name",
        widget = forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )
    email_address = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        label="Phone Number",
        widget=forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )
    postcode = forms.CharField(
        max_length=20,
        required=False,
        label="Postcode",
        widget=forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )
    tags = forms.CharField(
        required=False,
        label="Tags (comma-separated)",
        widget = forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )


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
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="First Name",
        widget = forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )
    email_address = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label="Phone Number",
        widget=forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )
    postcode = forms.CharField(
        max_length=20,
        required=False,
        label="Postcode",
        widget=forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )
    tags = forms.CharField(
        required=False,
        label="Tags (comma-separated)",
        widget = forms.TextInput(
            attrs={
                'class': 'form-inputs',
            }
        )
    )

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
    