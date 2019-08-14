import $ from "jquery";

window.jQuery = require("jquery");

window.$ = window.jQuery;

class hoverActions {
  static hover() {
    for (let row = 0; row < 100; row += 1) {
      const rowClass = `.row-${row}`;
      // Tried to refactor the callbacks into their own functions
      // however: https://stackoverflow.com/a/37893975
      $("body").on("mouseenter", rowClass, () => {
        if ($(rowClass).hasClass("error")) {
          $(rowClass).css({ background: "#DCDCDC", "background-color": "#DCDCDC" });
        } else {
          $(rowClass).css({ background: "#DCDCDC" });
        }
      });

      $("body").on("mouseleave", rowClass, () => {
        if ($(rowClass).hasClass("error")) {
          $(rowClass).css({ color: "#FB3D42", "background-color": "#FDF6F5" });
        } else {
          $(rowClass).css({ background: "white" });
        }
      });
    }
  }
}

export default hoverActions;
