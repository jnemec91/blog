
function shine() {
    console.log(this);
    this.parentNode.querySelector('.table-selected').classlist.remove('table-selected');
    this.classlist.add('table-selected');
}
