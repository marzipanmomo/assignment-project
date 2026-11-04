# forms for contacts page

from django import forms
from .models import ContactMessage
from accounts.validators import validate_email_domain

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'topic', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'contact-input'
        self.fields['name'].widget.attrs['placeholder'] = 'Your name'
        self.fields['email'].widget.attrs['placeholder'] = 'Your email'
        self.fields['message'].widget.attrs['placeholder'] = 'How can we help?'

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        validate_email_domain(email)
        return email