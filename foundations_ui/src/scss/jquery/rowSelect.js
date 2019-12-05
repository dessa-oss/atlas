import $ from 'jquery';

window.jQuery = require('jquery');

window.$ = window.jQuery;

class rowSelect {
  static retrieveRowElements(key) {
    return $(`.key-${key}`).toArray();
  }

  static removePreviousActiveRows() {
    $('.f9-active-row').removeClass('f9-active-row');
  }

  static select(key) {
    rowSelect.removePreviousActiveRows();
    const rowElements = rowSelect.retrieveRowElements(key);
    rowElements.forEach((el) => {
      $(el).addClass('f9-active-row');
    });
  }

  static deselect(key) {
    rowSelect.removePreviousActiveRows();
  }
}

export default rowSelect;
