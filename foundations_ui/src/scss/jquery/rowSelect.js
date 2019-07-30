import $ from 'jquery';

window.jQuery = require('jquery');

window.$ = window.jQuery;

class rowSelect {
  static retrieveRowElements(rowNumber) {
    const rowClassNumber = parseInt(rowNumber, 10);
    if (rowClassNumber >= 0) {
      return $(`.row-${rowClassNumber}`).toArray();
    }
    return [];
  }

  static removePreviousActiveRows() {
    $('.f9-active-row').removeClass('f9-active-row');
  }

  static select(rowNumber) {
    rowSelect.removePreviousActiveRows();
    const rowElements = rowSelect.retrieveRowElements(rowNumber);
    rowElements.forEach((el) => {
      // $(el).addClass('f9-active-row');
    });
  }

  static deselect(rowNumber) {
    rowSelect.removePreviousActiveRows();
  }
}

export default rowSelect;
