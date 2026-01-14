'use strict'

const navbarUpdate = function (event) {
    // if url is not the navbar update, update the navbar
    // console.log(event.target)
    // console.log(document.getElementById('navbar-wrap') !== event.target)

    // create navbar-wrap if it doesn't exist and append to body
    let wrap = document.getElementById('navbar-wrap')
    if (!wrap) {
        wrap = document.createElement('div')
        wrap.id = 'navbar-wrap'
        document.body.appendChild(wrap)
    }

    if (event.target.id !== 'navbar-wrap') {
        var navbar = document.getElementById('navbar-wrap')
        htmx.ajax('GET', '/update_navbar', {target:'#navbar-wrap', swap:'outerHTML'});
    }
}

document.addEventListener('htmx:afterSwap', function (event) {
    navbarUpdate(event);
});