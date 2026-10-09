# add the URL pattern for the sign-up view

from django.urls import path
from .views import signup_view
from django.contrib.auth.views import LoginView, LogoutView
from .forms import EmailLoginForm

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html', authentication_form=EmailLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# we are using django's built in LoginView and LogoutView so we dont need to create
# separate views in views.py