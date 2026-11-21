window.showToast = function(message, options){
    options = options || {};
    const region = document.getElementById('toast-region');
    if(!region) return;
    
    const toast = document.createElement('div');
    toast.className = "toast" + (options.type === 'error' ? ' toast-error' : '');

    const text = document.createElement('span');
    text.textContent = message;
    toast.appendChild(text);

    if (options.url){
        const link = document.createElement('a');
        link.href = options.url;
        link.textContent = options.text || 'View';
        toast.appendChild(link);
    }

    const close = document.createElement('button');
    close.type = 'button';
    close.className = 'toast-close';
    close.setAttribute('aria-label', 'Dismiss');
    close.textContent = 'x';
    close.addEventListener('click', function() {toast.remove();});
    toast.appendChild(close);

    region.appendChild(toast);
    setTimeout(function () {toast.remove(); }, 5000);
}