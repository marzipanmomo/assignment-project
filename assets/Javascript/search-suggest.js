(function () {
    let counter = 0;

    document.querySelectorAll('input[data-suggest-url]').forEach(function (input) {
        const wrap = input.parentElement;
        const list = wrap.querySelector('.suggest-list');
        const clear = wrap.querySelector('.search-clear');
        const form = input.form;
        const url = input.dataset.suggestUrl;
        const showAll = input.hasAttribute('data-suggest-all');
        const hadQuery = input.defaultValue.trim() !== '';   // the page was loaded with a search
        let timer = null;
        let controller = null;
        let activeIndex = -1;
        let allItems = null;                                 // cache of the "everything" list

        list.id = 'suggest-list-' + (++counter);
        list.setAttribute('role', 'listbox');
        input.setAttribute('role', 'combobox');
        input.setAttribute('aria-autocomplete', 'list');
        input.setAttribute('aria-controls', list.id);
        input.setAttribute('aria-expanded', 'false');

        function setOpen(open) {
            list.hidden = !open;
            input.setAttribute('aria-expanded', String(open));
            if (!open) activeIndex = -1;
        }

        function updateClear() {
            if (clear) clear.hidden = input.value === '';
        }

        function render(items) {
            list.innerHTML = '';
            items.forEach(function (item) {
                const li = document.createElement('li');
                li.setAttribute('role', 'option');
                const a = document.createElement('a');
                a.href = item.url;

                let thumb = null;
                if(item.image !== undefined){
                    thumb = document.createElement(item.image ? 'img' : 'span');
                    thumb.className = 'suggest-thumb';
                    if(item.image){
                        thumb.src = item.image;
                        thumb.alt = '';
                        thumb.width = 40;
                        thumb.height = 40;
                        thumb.loading = 'lazy'
                    }
                }

                const label = document.createElement('span');
                label.className = 'suggest-label'
                label.textContent = item.label;           // textContent, never innerHTML
                const kind = document.createElement('span');
                kind.className = 'suggest-kind';
                kind.textContent = item.kind;

                if(thumb) a.append(thumb, label, kind); else a.append(label, kind);
                li.appendChild(a);
                list.appendChild(li);
            });
            activeIndex = -1;
            setOpen(items.length > 0);
        }

        function load() {
            const q = input.value.trim();
            if (q === '' && !showAll) { setOpen(false); return; }
            if (q === '' && allItems) { render(allItems); return; }

            if (controller) controller.abort();
            controller = new AbortController();
            fetch(url + '?q=' + encodeURIComponent(q), { signal: controller.signal })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (q === '') allItems = data.suggestions;
                    if (document.activeElement !== input) return;   // user already moved on
                    render(data.suggestions);
                })
                .catch(function (err) {
                    if (err.name !== 'AbortError') console.error(err);
                });
        }

        input.addEventListener('input', function () {
            updateClear();
            clearTimeout(timer);
            timer = setTimeout(load, 150);
        });

        input.addEventListener('focus', function () {
            updateClear();
            load();
        });

        if (clear) {
            clear.addEventListener('click', function () {
                input.value = '';
                updateClear();
                // if this page is showing results for a search, reset them
                if (hadQuery && form) {
                    if (form.requestSubmit) form.requestSubmit(); else form.submit();
                    return;
                }
                input.focus();
                load();
            });
        }

        input.addEventListener('keydown', function (e) {
            const links = list.querySelectorAll('a');
            if (e.key === 'Escape') { setOpen(false); return; }
            if (list.hidden || !links.length) return;

            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                e.preventDefault();
                const step = e.key === 'ArrowDown' ? 1 : -1;
                activeIndex = (activeIndex + step + links.length) % links.length;
                links.forEach(function (l, i) {
                    l.parentElement.classList.toggle('active', i === activeIndex);
                });
                links[activeIndex].scrollIntoView({ block: 'nearest' });
            } else if (e.key === 'Enter' && activeIndex >= 0) {
                e.preventDefault();
                links[activeIndex].click();
            }
        });

        document.addEventListener('click', function (e) {
            if (!wrap.contains(e.target)) setOpen(false);
        });

        //if you press enter, then back button to home page, search box will not be activated.
        if(form){
            form.addEventListener('submit', function(){
                setOpen(false);
                input.blur();
            });
        }

        window.addEventListener('pageshow', function(){
            setOpen(false);
            if(showAll) input.value = input.defaultValue;
            if(document.activeElement === input) input.blur();
            updateClear();
        });

        updateClear();
    });
})();