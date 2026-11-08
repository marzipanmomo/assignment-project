from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from .models import Product, Category

# Create your views here.
@login_required
def home_view(request):
    featured = Product.objects.filter(is_featured=True)[:4]
    return render(request, 'store/home.html', {'featured': featured})

@login_required
def categories_view(request):
    return render(request, 'store/categories.html')

#redirect after successful post, pre-filling form account for logged in users
#did not add @login_required so that visitors can contact without an account

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! We've received your message and will reply soon.")
            return redirect('contact')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'name': f"{request.user.first_name} {request.user.last_name}".strip(),
                'email': request.user.email,
            }
        form = ContactForm(initial=initial)
    return render(request, 'store/contact.html', {'form': form})
