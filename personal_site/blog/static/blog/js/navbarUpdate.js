'use strict'

document.addEventListener('htmx:afterSwap', function (event) {
    // if url is not the navbar update, update the navbar
    // console.log(event.target)
    // console.log(document.getElementById('navbar-wrap') !== event.target)
    if (event.target !== document.getElementById('navbar-wrap')) {
        var navbar = document.getElementById('navbar-wrap')
        if (navbar) {
            // console.log('updating navbar')
            // use htmx ajax to get the navbar from the server, and swap content in #navbar-block
            htmx.ajax('GET', '/update_navbar', {target:'#navbar-wrap', swap:'innerHTML'});
        }
    }
})