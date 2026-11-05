// Header nav dropdowns (Solutions, Support, Showcase). Each button
// "#dropbtn-<Name>" toggles "#<Name>_dropdown". Only one menu is open at a
// time, and a click anywhere outside a dropdown button closes them all.

function setDropdownOpen(button, open) {
    var menu = document.getElementById(button.id.replace(/^dropbtn-/, '') + '_dropdown');
    if (menu) {
        menu.classList.toggle('show', open);
    }
    button.classList.toggle('opened', open);
    button.setAttribute('aria-expanded', open ? 'true' : 'false');
}

function closeDropdowns(except) {
    document.querySelectorAll('.dropdown-menu-item > button[id^="dropbtn-"]').forEach(function (button) {
        if (button !== except) {
            setDropdownOpen(button, false);
        }
    });
}

function clickDropdown(name) {
    var button = document.getElementById('dropbtn-' + name);
    if (!button) {
        return;
    }
    closeDropdowns(button);
    setDropdownOpen(button, !button.classList.contains('opened'));
}

window.addEventListener('click', function (event) {
    if (!event.target.closest('.dropdown-menu-item > button[id^="dropbtn-"]')) {
        closeDropdowns(null);
    }
});
