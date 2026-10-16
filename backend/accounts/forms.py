from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

# allowed email domains for validation purposes
ALLOWED_EMAIL_DOMAINS = {
    'gmail.com',
    'outlook.com',
    'hotmail.com',
    'yahoo.com',
    'icloud.com',
}

# form for sign up
class CustomUserCreationForm(UserCreationForm):
    # modified django's UserCreationForm to add extra fields, remove username
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        # fields i want to include
        fields = ('first_name', 'last_name', 'email')

    # loops through all form fields and adds css class form-input for styling

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

        # checks if field exists, puts placeholders inside the boxes
        if 'first_name' in self.fields:
            self.fields['first_name'].widget.attrs.update({
                'placeholder': 'First Name',
                'autocomplete': 'off'
            })

        if 'last_name' in self.fields:
            self.fields['last_name'].widget.attrs.update({
                'placeholder': 'Last Name',
                'autocomplete': 'off'
            })

        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({
                'placeholder': 'Email',
                'autocomplete': 'email'
            })

        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'placeholder': 'Password',
                'autocomplete': 'new-password'
            })

        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'placeholder': 'Confirm Password',
                'autocomplete': 'new-password'
            })

    #prevent error caused by duplicate email, if you try to use one email to make 2 accounts
    #will also make email lowercase so now it's case insensitive
    #updated to allow email format validation
    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        domain = email.rsplit('@', 1)[1] # splits by @ and takes 2nd part
        if domain not in ALLOWED_EMAIL_DOMAINS:
            raise forms.ValidationError(
                "Please use an email from a supported provider (e.g. gmail.com)."
            )

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    #django's db requires username so this method assigns a username before saving to db
    def save(self, commit=True):
        user = super().save(commit=False)
        # removing username field by automatically assigning email to username
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

#form for log in
class EmailLoginForm(AuthenticationForm):
    #expands Django's built in Authentication form
    #allows login using email instead of username
    #overrides username field as email field
    username = forms.EmailField(label="Email")

    #to separate components for stylesheet
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({
                'placeholder': 'Email',
                'autocomplete': 'email'
            })
        
        if 'password' in self.fields:
            self.fields['password'].widget.attrs.update({
                'placeholder': 'Password',
                'autocomplete': 'current-password'
            })

    #converts email login to lowercase to compare with emails in db record
    def clean_username(self):
        #lower case to match the emails stored in the database
        return self.cleaned_data['username'].lower()

    #init runs when the form object is created, and adds form input class to each fields widget
    