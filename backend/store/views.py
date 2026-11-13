from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from .models import Product, Category
from django.db.models import Q, Count

# Create your views here.

def home_view(request):
    featured = Product.objects.filter(is_featured=True)[:4]
    return render(request, 'store/home.html', {'featured': featured})

def categories_view(request):
    return render(request, 'store/categories.html', {
        'rooms': Category.objects.filter(group='room'),
        'aesthetics': Category.objects.filter(group='aesthetic'),
        'types': Category.objects.filter(group='type'),
    })

def category_detail_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': category.products.all(),
    })

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

def products_view(request):
    query = request.GET.get('q', '').strip()
    room = request.GET.get('room', '')
    aesthetic = request.GET.get('aesthetic', '')
    ptype = request.GET.get('type', '')

    products = Product.objects.all()
    
    # allows you to search filter names/shorter words too
    for word in query.split():
        products = products.filter(
            Q(name__icontains=word) 
            | Q(description__icontains=word)
            | Q(option__icontains=word)
            | Q(categories__name__icontains=word)
        )

    if room:
        products = products.filter(categories__slug=room)
    if aesthetic:
        products = products.filter(categories__slug=aesthetic)
    if ptype:
        products = products.filter(categories__slug=ptype)

    return render(request, 'store/products.html', {
        'products': products.distinct(),
        'query': query,
        'rooms': Category.objects.filter(group='room'),
        'aesthetics': Category.objects.filter(group='aesthetic'),
        'types': Category.objects.filter(group='type'),
        'selected_room': room,
        'selected_aesthetic': aesthetic,
        'selected_type': ptype,
    })

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # other products (ranked by how mant categories they share)
    related = (
        Product.objects.filter(categories__in=product.categories.all())
        .exclude(pk=product.pk)
        .annotate(shared=Count('categories'))
        .order_by('-shared', 'name')[:4]
    )

    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
    })