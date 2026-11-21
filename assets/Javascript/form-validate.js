document.querySelectorAll('form[data-validate]').forEach(function(form){
    const fields = Array.from(form.querySelectorAll(
        'input:not([type=hidden]):not([type=sumbit]):not([type=button]), select, textarea'  
    )).filter(function(f){ return f.name; });

    function label(input){
        const l = input.labels && input.labels[0];
        return input.dataset.label || input.placeholder || (l && l.textContent.trim()) || 'This field';
    }

    function messageFor(input){
        const v = input.validity;
        if (v.valueMissing) return label(input) + ' is required.';
        if (v.typeMismatch && input.type === 'email'){
            return 'Enter a valid email address, like name@example.com.';
        }
        if (v.tooShort) return label(input) + ' must be at least ' + input.minLength + ' characters.';
        if (input.dataset.match) {
            const other = document.getElementById(input.dataset.match);
            if (other && input.value !== other.value) return 'The passwords do not match.';
        }
        return ''
    }

    function anchor(input){ return input.closest('.password-wrapper') || input;}

    function clearError(input) {
        input.removeAttribute('aria-invalid');
        let next = anchor(input).nextElementSibling;
        while(next && (next.classList.contains('field-error') || next.classList.contains('errorlist'))){
           const after=next.nextElementSibling; 
            next.remove();
            next = after;
        }
    }

    function showError(input, message){
        clearError(input);
        input.setAttribute('aria-invalid', 'true');
        const p = document.createElement('p');
        p.className = 'field-error';
        p.setAttribute('role', 'alert');
        p.textContent = message;
        anchor(input).after(p);
    }

    function check(input) {
        const message = messageFor(input);
        if (message) { showError(input, message); return false;}
        clearError(input);
        return true;
    }

    fields.forEach(function(input){
        input.addEventListener('blur', function(){
            if(input.value || input.hasAttribute('aria-invalid')) check(input);
        });
        input.addEventListener('input', function(){
            if(input.hasAttribute('aria-invalid')) check(input); else clearError(input);
        });
    });

    form.addEventListener('submit', function(e){
        let firstBad = null;
        fields.forEach(function(input){
            if(!check(input) && !firstBad) firstBad = input;
        });
        if(firstBad) {e.preventDefault(); firstBad.focus();}
    });
});