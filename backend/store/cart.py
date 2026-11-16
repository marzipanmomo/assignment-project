from .models import Product

CART_KEY = 'cart'
MAX_QTY = 99

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(CART_KEY, {}) #{"12": 2, ...}
    def _save(self):
        self.session[CART_KEY] = self.cart 
        self.session.modified = True

    def add(self, product, quantity=1):
        pid = str(product.pk)
        self.cart[pid] = min(self.cart.get(pid,0) + quantity, MAX_QTY)
        self._save()

    def set_quantity(self, product, quantity):
        pid = str(product.pk)
        if quantity > 0:
            self.cart[pid] = min(quantity, MAX_QTY)
        else:
            self.cart.pop(pid, None)
        self._save()

    def remove(self, product):
        self.cart.pop(str(product.pk), None)
        self._save()

    def clear(self):
        self.session.pop(CART_KEY, None)
        self.session.modified = True

    def __iter__(self):
        for product in Product.objects.filter(pk__in=self.cart.keys()):
            qty = self.cart[str(product.pk)]
            yield{'product': product, 'quantity': qty, 'subtotal': product.price * qty}

    def __len__(self):
        return sum(self.cart.values())

    def total(self):
        return sum(item['subtotal'] for item in self)

    # get and _save are so that users who never touch the cart don't have a session created for them