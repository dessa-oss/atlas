import $ from 'jquery';

window.jQuery = require('jquery');

window.$ = window.jQuery;

class changeIcon {
  static changeIconByAccessor(elementAccessor, iconClass) {
    $(elementAccessor).attr('class', iconClass);
  }

  static changeIconByAccessorAndDisabled(elementAccessor, iconClass) {
    changeIcon.changeIconByAccessor(elementAccessor, iconClass);
    $(elementAccessor).attr('disabled', true);
  }

  static changeIconByAccessorAndEnabled(elementAccessor, iconClass) {
    changeIcon.changeIconByAccessor(elementAccessor, iconClass);
    $(elementAccessor).prop('disabled', true);
    $(elementAccessor).removeAttr('disabled');
  }
}

export default changeIcon;
