# add the URL pattern for the sign-up view

from django.urls import path
from .views import signup_view, EmailLoginView, EmailLogoutView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', EmailLogoutView.as_view(), name='logout'),
]

''' we made custom sign up view, email login view and email logout view so that 
when sign up redirects to login it auto-fills the email without google password manager,
plus when you logout the email is also auto-filled in the login page'''