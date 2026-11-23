document.querySelectorAll('form[data-cart-add').forEach(function(form){
    form.addEventListener('submit', function(e){
        if (e.defaultPrevented) return;
        e.preventDefault();
        const button = form.querySelector('button[type="submit"]');
        button.disabled = true;
        button.textContent = 'Adding...';

        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {'X-Requested-With': 'XMLHttpRequest'},
        })
        .then(function(response){
            if(!response.ok) throw new Error('Request failed');
            return response.json();
        })
        .then(function(data){
            document.querySelectorAll('[data-cart-count]').forEach(function(el){
                el.textContent = data.count;
            });

            //form turns into view cart link
            const link = document.createElement('a');
            link.href = data.cart_url;
            link.className = 'add-to-cart-btn view-cart-btn';
            link.textContent = 'View cart';
            form.replaceWith(link);

            window.showToast(data.name + ' was added to your cart.', { url: data.cart_url, text: 'View cart' });
        })
        .cath(function(){
            button.disabled = false;
            button.textContent = 'Add to cart';
            window.showToast("Sorry, we couldn't add that to your cart. Please try again.", { type: 'error' });
        });
    });
});