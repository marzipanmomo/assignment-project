document.querySelectorAll('.toggle-password').forEach(function(button){
    button.addEventListener('click',function(){
        const input = button.previousElementSibling;

        if(input.type === 'password'){
            input.type = 'text';
            button.textContent = 'Hide';
        }
        else{
            input.type = 'password';
            button.textContent = 'Show';
        }
    });
});