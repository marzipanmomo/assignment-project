# add the URL pattern for the sign-up view

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import signup_view, EmailLoginView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# we are using django's built in LogoutView for now
# we made custom sign up view and email login view so that 
# when sign up redirects to login it auto-fills the email without google password manager