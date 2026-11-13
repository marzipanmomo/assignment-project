const scrollBtn = document.getElementById('scroll-top');

//show button when page scrolls down a bit
window.addEventListener('scroll', function(){
    scrollBtn.classList.toggle('visible', window.scrollY > 300);
});

//scroll to top when you click the button
scrollBtn.addEventListener('click', function(){
    window.scrollTo({top: 0, behavior: 'smooth' });
});
