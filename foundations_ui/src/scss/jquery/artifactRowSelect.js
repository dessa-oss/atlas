import $ from 'jquery';

window.jQuery = require('jquery');

window.$ = window.jQuery;

class artifactRowSelect {
  static removePreviousActiveRows() {
    $('.artifact-active-row').removeClass('artifact-active-row');
  }

  static select(key) {
    artifactRowSelect.removePreviousActiveRows();
    key = key.replace('.', '\\.');
    $(`#${key}`).addClass('artifact-active-row');
  }

  static deselect(key) {
    artifactRowSelect.removePreviousActiveRows();
  }
}

export default artifactRowSelect;
