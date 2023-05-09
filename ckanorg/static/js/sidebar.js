// Sidebar open/close logic
var click = document.querySelector('#st-button');
var close = document.querySelector('#st-button-close');
var menu = document.querySelector('#st-container');
var pusher = document.querySelector('.st-pusher');

click.addEventListener('click', addClass);
close.addEventListener('click', function() {
    menu.classList.toggle('st-menu-open');
});
pusher.addEventListener('click', closeMenu);

function addClass(e) {
    menu.classList.toggle('st-menu-open');
}

function closeMenu(el) {
    // if the click target has this class then we close the menu by removing all the classes
    if (el.target.classList.contains('st-pusher')) {
        menu.classList.toggle('st-menu-open');
    }
}