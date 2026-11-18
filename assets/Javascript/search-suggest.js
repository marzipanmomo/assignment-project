document.querySelectorAll('input[data-suggest-url]').forEach(function(input){
    const list = input.parentElement.querySelector('.suggest-list');
    const url = input.dataset.suggestUrl;
    let timer = null;
    let controller = null;
    let activeIndex = -1;

    function hide(){
        list.hidden = true;
        list.innerHTML = '';
        activeIndex = -1;
    }

    function render(items){
        list.innerHTML = '';
        items.forEach(function(item) {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = item.url;

            const label = document.createElement('span');
            label.textContent = item.label;
            const kind = document.createElement('span');
            kind.className = 'suggest-kind';
            kind.textContent = item.kind;

            a.append(label, kind);
            li.appendChild(a);
            list.appendChild(li);
        });
        list.hidden = items.length === 0;
        activeIndex = -1;
    }

    //wait 200ms, cancel any inflight requests

    input.addEventListener('input', function (){
        clearTimeout(timer);
        const q = input.value.trim();
        if (q.length < 2) {hide(); return;}

        timer = setTimeout(function(){
            if (controller) controller.abort();
            controller = new AbortController();
            fetch(url + '?q=' + encodeURIComponent(q), { signal: controller.signal })
            .then(function (r) { return r.json(); })
            .then(function (data) { render(data.suggestions); })
            .catch(function (err) {
                if (err.name !== 'AbortError') console.error(err);
            });
        }, 200);
    });

    // arrow keys to move through the list, enter to press
    input.addEventListener('keydown', function (e) {
        const links = list.querySelectorAll('a');
        if (list.hidden || !links.length) return;

        if (e.key === 'ArrowDown' || e.key === 'ArrowUp'){
            e.preventDefault();
            const step = e.key === 'ArrowDown' ? 1 : -1;
            activeIndex = (activeIndex + step + links.length) % links.length;
            links.forEach(function (l, i) {
                l.parentElement.classList.toggle('active', i === activeIndex);   
            });
        } else if (e.key === 'Enter' && activeIndex >= 0) {
            e.preventDefault();
            links[activeIndex].click();
        } else if (e.key === 'Escape') {
            hide();
        }
    });

    document.addEventListener('click', function(e){
        if(!input.parentElement.contains(e.target)) hide();
    });
});