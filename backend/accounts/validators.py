# email validation stored here so it can be imported by login/signup and contact pages

from django import forms
from django.conf import settings
from email_validator import validate_email, EmailNotValidError

TYPO_DOMAINS = {
    'gmial.com': 'gmail.com', 'gmai.com': 'gmail.com', 'gamil.com': 'gmail.com',
    'g-mail.com': 'gmail.com', 'gmail.co': 'gmail.com', 'gmail.cot': 'gmail.com',
    'gmail.con': 'gmail.com', 'hotmial.com': 'hotmail.com', 'hotmail.con': 'hotmail.com',
    'outlok.com': 'outlook.com', 'outlook.con': 'outlook.com',
    'yaho.com': 'yahoo.com', 'yahooo.com': 'yahoo.com', 'yahoo.con': 'yahoo.com',
    'icloud.con': 'icloud.com',
}

def validate_email_domain(email):
    domain = email.lower().rsplit('@', 1)[-1]

    fix = TYPO_DOMAINS.get(domain)

    if fix:
        raise forms.ValidationError(f"Did you mean @{fix}?")

    try:
        validate_email(
            email,
            check_deliverability=getattr(settings, 'CHECK_EMAIL_DOMAINS', True),
            timeout=5,   
        )
    except EmailNotValidError:
        raise forms.ValidationError(
            f"We couldn't verify that {domain} can receive email. Please check the spelling."
        )