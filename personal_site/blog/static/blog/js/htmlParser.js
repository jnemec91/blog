'use strict';

// this function will parse html preview to another div in the same page.
// it will do it on change of textarea
function parseHtml(textarea) {
    var html = textarea.value;
    var preview = document.getElementById('post-preview');
    preview.innerHTML = html;
}