(function(){
    const form = document.getElementById('filter-form');
    if(!form) return;

    const input = form.querySelector('input[name="q"]');
    const clear = form.querySelector('.search-clear');
    const selects = form.querySelectorAll('select');
    const reset = document.getElementById('filter-reset');
    const status = document.getElementById('results-status');
    const results = document.getElementById('results');
    const TARGETS = ['results-heading', 'results'];

    let timer = null;
    let controller = null;

    function currentParams(){
        const params = new URLSearchParams();
        new FormData(form).forEach(function(value, key){
            if(typeof value === 'string' && value.trim() !== '') params.append(key, value.trim());
        });
        return params;
    }

    function syncControls(){
        if (clear) clear.hidden = input.value === '';
        if (reset) reset.disabled = currentParams().toString() === '';   
    }

    function update(){
        clearTimeout(timer);
        syncControls();

        const qs = currentParams().toString();
        const url = location.pathname + (qs ? '?' + qs: '');

        if(controller) controller.abort();
        controller = new AbortController();
        results.classList.add('loading');

        fetch(url, {
            headers: {'X-Requested-With': 'XMLHttpRequest'},
            signal: controller.signal,
        })
            .then(function(response){
                if(!response.ok) throw new Error('Bad response');
                return response.text();
            })
            .then(function(html){
                const doc = new DOMParser().parseFromString(html, 'text/html');
                TARGETS.forEach(function(id){
                    const fresh = doc.getElementById(id);
                    const current = document.getElementById(id);
                    if(fresh && current) current.innerHTML = fresh.innerHTML;
                });
                const count = doc.querySelector('.result-count');
                if(status && count) status.textContent = count.textContent.trim();
                history.replaceState(null, '', url);
                results.classList.remove('loading');
            })
            .catch(function(err){
                if(err.name === 'AbortError') return;
                location.href = url;
            });
    }

    input.addEventListener('input', function(){
        syncControls();
        clearTimeout(timer);
        timer = setTimeout(update, 250);
    });

    selects.forEach(function(select){
        select.addEventListener('change', update);
    });

    form.addEventListener('submit', function(e){
        e.preventDefault();
        update();
    });

    if(clear){
        clear.addEventListener('click', function(){
            input.value = '';
            input.focus();
            update();
        });
    }

    if(reset){
        reset.addEventListener('click', function(e){
            e.preventDefault();
            input.value = '';
            selects.forEach(function(select){ select.value = ''; });
            update();
        });
    }

    results.addEventListener('click', function(e){
        const link = e.target.closest('.active-filters a');
        if(!link) return;
        e.preventDefault();
        const params = new URL(link.href).searchParams;
        input.value = params.get('q') || '';
        selects.forEach(function(select){ select.value = params.get(select.name) || ''; });
        update();
    });

    syncControls();
})();