from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home_view(request):
    return render(request, 'store/home.html')

@login_required
def categories_view(request):
    return render(request, 'store/categories.html')