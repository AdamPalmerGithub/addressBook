from django import forms
from .models import Contact, Tag

class ContactForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email_address', 'phone_number', 'postcode', 'tags']
