import $ from 'jquery';

window.jQuery = require('jquery');

window.$ = window.jQuery;

class rowSelect {
  static handleTransition(rowClass, row) {
    if ($(rowClass).hasClass('error')) {
      console.log('Handle the selection for row with error');
    } else {
      console.log('Handle the selection of a row without error');
    }
  }

  static retrieveRowElements(rowNumber) {
    const rowClassNumber = parseInt(rowNumber, 10);
    console.log(rowClassNumber);
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
      $(el).addClass('f9-active-row');
    });
  }

  static deselect(rowNumber) {
    rowSelect.removePreviousActiveRows();
  }
}

export default rowSelect;
