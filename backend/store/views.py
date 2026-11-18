from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from .models import Product, Category
from django.db.models import Q, Count, Case, When, Value, IntegerField
from .search import word_query, word_variants, suggest_query
from urllib.parse import urlencode
from django.views.decorators.http import require_POST
from .cart import Cart
from django.http import JsonResponse
from django.urls import reverse

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
            request.session['contact_sent'] = True
            return redirect('contact')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'name': f"{request.user.first_name} {request.user.last_name}".strip(),
                'email': request.user.email,
            }
        form = ContactForm(initial=initial)

    sent = request.session.pop('contact_sent', False)
    
    return render(request, 'store/contact.html', {'form': form, 'sent': sent})

SORTS = {
    'price_asc': ('Price: low to high', ('price', 'name')),
    'price_desc': ('Price: high to low', ('-price', 'name')),
    'name': ('Name: A to Z', ('name',)),
}

def products_view(request):
    query = request.GET.get('q', '').strip()
    room = request.GET.get('room', '')
    aesthetic = request.GET.get('aesthetic', '')
    ptype = request.GET.get('type', '')
    sort = request.GET.get('sort', '')

    products = Product.objects.all()
    
    # allows you to search filter names/shorter words too
    for word in query.split():
        products = products.filter(word_query(word))

    if room:
        products = products.filter(categories__slug=room)
    if aesthetic:
        products = products.filter(categories__slug=aesthetic)
    if ptype:
        products = products.filter(categories__slug=ptype)

    products = products.distinct()

    if sort in SORTS:
        products = products.order_by(*SORTS[sort][1])
    elif query:
        # name matches will come before description matches
        name_hits = Q()
        for word in query.split():
            for v in word_variants(word):
                name_hits |= Q(name__icontains=v)
        products = products.annotate(
            name_match=Case(
                When(name_hits, then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by('name_match', 'name')

    #active filter tags, each with a link that removes just that filter

    params = {'q': query, 'room': room, 'aesthetic': aesthetic, 'type': ptype, 'sort': sort}

    def without(key):
        rest = {k: v for k, v in params.items() if v and k != key}
        return '?' + urlencode(rest) if rest else ''

    names = {c.slug: c.name for c in Category.objects.filter(
        slug__in=[s for s in (room, aesthetic, ptype) if s])}

    active = []

    if query:
        active.append({'label': f'{query}', 'remove': without('q')})
    if room:
        active.append({'label': names.get(room, room), 'remove': without('room')})
    if aesthetic:
        active.append({'label': names.get(aesthetic, aesthetic), 'remove': without('aesthetic')})
    if ptype:
        active.append({'label': names.get(ptype, ptype), 'remove': without('type')})

    suggestion = suggest_query(query) if query and not products.exists() else None

    return render(request, 'store/products.html', {
        'products': products,
        'query': query,
        'rooms': Category.objects.filter(group='room'),
        'aesthetics': Category.objects.filter(group='aesthetic'),
        'types': Category.objects.filter(group='type'),
        'selected_room': room,
        'selected_aesthetic': aesthetic,
        'selected_type': ptype,
        'selected_sort': sort,
        'sort_options': [(k, v[0]) for k, v in SORTS.items()],
        'active': active,
        'suggestion': suggestion,
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

def cart_view(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {
        'items': list(cart),
        'total': cart.total(),
    })

@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        quantity = max(int(request.POST.get('quantity', 1)), 1)
    except ValueError:
        quantity = 1
    Cart(request).add(product, quantity)
    return redirect('cart')

@require_POST
def cart_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
    Cart(request).set_quantity(product, quantity)
    return redirect('cart')

@require_POST
def cart_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Cart(request).remove(product)
    return redirect('cart')

# require post protext against forged requests, or being triggered by plain links

def search_suggestions(request):
    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        return JsonResponse({'suggestions': []})

    # product matches
    products = Product.objects.all()
    for word in query.split():
        name_q = Q()
        for v in word_variants(word):
            name_q |= Q(name__icontains=v)
        products = products.filter(name_q)

    results = [
        {'label': p.name, 'kind': 'Product',
         'url': reverse('product_detail', args=[p.pk])}
         for p in products.order_by('name')[:5]
    ]

    results += [
        {'label': c.name, 'kind': 'Category',
         'url': reverse('category_detail', args=[c.slug])}
        for c in Category.objects.filter(name__icontains=query)[:3]
    ]

    # if nothing found suggest typo correction

    if not results:
        fix = suggest_query(query)
        if fix:
            results.append({
                'label': fix, 'kind': 'Did you mean',
                'url': reverse('products') + '?' + urlencode({'q': fix}),
            })

    return JsonResponse({'suggestions': results})