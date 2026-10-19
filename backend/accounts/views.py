from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, EmailLoginForm

# Create your views here.

# Auto-fill the email in the login page when redirected
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # remember email so login page can pre-fill it
            # saves email into session before redirecting
            request.session['signup_email'] = form.cleaned_data['email']
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# get initial runs when the login form is built, reads the
# email out of the session, removes it with pop
# uses it as starting value of the username field
class EmailLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailLoginForm

    def get_initial(self):
        initial = super().get_initial()
        email = self.request.session.pop('signup_email', None)
        if email:
            initial['username'] = email
        return initial

# same thing for log out
class EmailLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        # grab email before session is cleared
        email = request.user.email if request.user.is_authenticated else None
        response = super().post(request, *args, **kwargs)
        if email:
            # session is fresh after logout, so store it again
            request.session['signup_email'] = email
        return response