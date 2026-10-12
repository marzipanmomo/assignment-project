from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        # fields i want to include
        fields = ('first_name', 'last_name', 'email')

    #this code is so that we can call individual components of the usercreationform
    #as a class for the stylesheet

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

        # writing inside the boxes
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
                'placeholder': '********',
                'autocomplete': 'new-password'
            })

        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'placeholder': '********',
                'autocomplete': 'new-password'
            })

    #prevent error caused by duplicate email, if you try to use one email to make 2 accounts
    #will also make email lowercase so now it's case insensitive
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # removing username field by automatically assigning email to username
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EmailLoginForm(AuthenticationForm):
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
                'placeholder': '********',
                'autocomplete': 'current-password'
            })

    def clean_username(self):
        #lower case to match the emails stored in the database
        return self.cleaned_data['username'].lower()

    #init runs when the form object is created, and adds form input class to each fields widget
    