import $ from 'jquery';

window.jQuery = require('jquery');

window.$ = window.jQuery;

class hoverActions {
  static onMouseEnter(rowClass, row) {
    if ($(rowClass).hasClass('error')) {
      $(rowClass).css({ background: '#DCDCDC', 'background-color': '#DCDCDC' });
    } else {
      $(rowClass).css({ background: '#DCDCDC' });
    }
  }

  static onMouseLeave(rowClass, row) {
    if ($(rowClass).hasClass('error')) {
      $(rowClass).css({ color: '#FB3D42', 'background-color': '#FDF6F5' });
    } else {
      $(rowClass).css({ background: 'white' });
    }
  }

  static hover() {
    for (let row = 0; row < $('.job-table-row').length / 3; row += 1) {
      const rowClass = `.row-${row}`;
      $('body').on('mouseenter', rowClass, () => hoverActions.onMouseEnter(rowClass, row));
      $('body').on('mouseleave', rowClass, () => hoverActions.onMouseLeave(rowClass, row));
    }
  }
}

export default hoverActions;
