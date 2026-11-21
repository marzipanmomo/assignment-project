(function(){
    const root = document.documentElement;
    const KEY = 'theme';
    const media = window.matchMedia('(prefers-color-scheme: dark)');

    function saved(){
        try{
            const value = localStorage.getItem(KEY);
            return value === 'dark' || value === 'light' ? value : null;  
        } catch (e) {return null;}
    }

    function apply(theme){
        root.setAttribute('data-theme', theme);
        document.querySelectorAll('[data-theme-toggle]').forEach(function (btn){
           btn.setAttribute('aria-pressed', String(theme === 'dark'));
        });
    }

    // run while page still loading, so no flash of wrong theme

    apply(saved() || (media.matches ? 'dark' : 'light'));

    document.addEventListener('DOMContentLoaded', function(){
        apply(root.getAttribute('data-theme'));
        document.querySelectorAll('[data-theme-toggle]').forEach(function(btn){
            btn.addEventListener('click', function(){
                const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
                apply(next);
                try{localStorage.setItem(KEY, next);} catch(e){}
            });
        });
    });

    // follow os setting until vistor changes
    media.addEventListener('change', function(e){
        if(!saved()) apply(e.matches ? 'dark': 'light');
    });
})();