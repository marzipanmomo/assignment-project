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

        self.fields['name'].error_messages['required'] = "Please enter your name."
        self.fields['email'].error_messages['required'] = "Please enter your email."
        self.fields['email'].error_messages['invalid'] = "That doesn't look like a valid email address."
        self.fields['message'].error_messages['required'] = "Please tell us how we can help."
                
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        validate_email_domain(email)
        return email

    def clean_message(self):
        message = self.cleaned_data['message'].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please write at least 10 characters so we can help properly.")
        return message