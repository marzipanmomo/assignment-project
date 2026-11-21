(function(){
    const dialog = document.getElementById('confirm-dialog');
    if(!dialog) return;

    const text = document.getElementById('confirm-text');
    const okButton = document.getElementById('confirm-ok');
    let pendingForm = null;

    document.querySelectorAll('form[data-confirm]').forEach(function(form){
      form.addEventListener('submit', function(e){
        e.preventDefault();
        pendingForm = form;
        text.textContent = form.dataset.confirm;
        dialog.showModal();
      });  
    });

    okButton.addEventListener('click', function(){
        const form = pendingForm;
        pendingForm = null;
        dialog.close();
        if(form) form.submit();
    });

    dialog.querySelectorAll('[data-modal-cancel]').forEach(function(btn){
        btn.addEventListener('click', function(){ dialog.close();});
    });

    // click outside modal
    dialog.addEventListener('click', function(e){
      if(e.target === dialog) dialog.close();
    })

    dialog.addEventListener('close', function(){pendingForm = null;});
})();