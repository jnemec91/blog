'use strict';

function updateSearchUrl(url) {
    const searchValue = document.getElementById('search-input').value;
    const searchButton = document.getElementById('search-button');
    // Update hx-get to dynamically include the search phrase
    let search_url = url + searchValue;
    htmx.ajax('get', search_url, {target:'#page_content', swap:'outerHTML'});
}