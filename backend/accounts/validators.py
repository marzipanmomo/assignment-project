# email validation stored here so it can be imported by login/signup and contact pages

from django import forms

ALLOWED_EMAIL_DOMAINS = {
    'gmail.com',
    'outlook.com',
    'hotmail.com',
    'yahoo.com',
    'icloud.com',
    'protonmail.com'
}

def validate_email_domain(email):
    domain = email.lower().rsplit('@', 1)[1]
    if domain not in ALLOWED_EMAIL_DOMAINS:
        raise forms.ValidationError(
            "Please use an email from a supported provider (e.g. gmail.com)."
        )